// 简单前端逻辑：在内存保存 access token，refresh token 存 httpOnly cookie（由服务端设置）
// 与后端交互的端点：POST /api/login, POST /api/refresh, POST /api/logout, GET /api/me
type LoginRequest = { username: string; password: string };
type TokenResponse = { access_token: string; expires_in: number; token_type?: string };
type UserOut = { id: number; username: string };

const API_BASE = "http://localhost:8000"; // 后端地址，按需修改

let accessToken: string | null = null; // 仅内存保存，避免 localStorage 的 XSS 风险

// UI 元素
const registerPage = document.getElementById("registerPage") as HTMLElement;
const loginPage = document.getElementById("loginPage") as HTMLElement;
const homePage = document.getElementById("homePage") as HTMLElement;
const loadingDiv = document.getElementById("loading") as HTMLElement;
const welcomeP = document.getElementById("welcome") as HTMLElement;

const registerForm = document.getElementById("registerForm") as HTMLFormElement;      // 前端点击登录，会返回这个对象
const loginForm = document.getElementById("loginForm") as HTMLFormElement;      // 前端点击登录，会返回这个对象
const btnInfo = document.getElementById("btnInfo") as HTMLButtonElement;
const btnLogout = document.getElementById("btnLogout") as HTMLButtonElement;

function showPage(id: "register" | "login" | "home" | "loading") {
  loginPage.classList.toggle("hidden", id !== "login");
  registerPage.classList.toggle("hidden", id !== "register");
  homePage.classList.toggle("hidden", id !== "home");
  loadingDiv.classList.toggle("hidden", id !== "loading");
}

function setAccessToken(token: string | null) {
  accessToken = token;
  if (token) {
    welcomeP.textContent = "已登录（access token 在内存中）";
  } else {
    welcomeP.textContent = "";
  }
}

// fetch wrapper：自动带 Authorization header；遇 401 尝试 refresh 并重试一次
async function apiFetch(input: RequestInfo, init: RequestInit = {}, retry = true): Promise<Response> {
  const headers = new Headers(init.headers || {});
  if (accessToken) {
    headers.set("Authorization", `Bearer ${accessToken}`);
  }
  // 注意：对于需要携带 httpOnly refresh cookie 的请求（/api/refresh 或 /api/logout），必须设置 credentials: 'include'
  const cfg: RequestInit = {
    ...init,
    headers,
    credentials: init.credentials ?? "include", // 默认允许带 cookie（refresh 存在时需要）
  };

  let resp = await fetch(`${API_BASE}${input}`, cfg);
  if (resp.status === 401 && retry) {
    // 尝试用 refresh 换取新的 access_token
    const refreshed = await tryRefresh();
    if (refreshed) {
      // 重试原请求一次（但不再无限重试）
      return apiFetch(input, init, false);
    }
  }
  return resp;
}

// 调用 /api/refresh，从 cookie 中读取 refresh token（httpOnly），并获取新的 access token
async function tryRefresh(): Promise<boolean> {
  try {
    const resp = await fetch(`${API_BASE}/api/refresh`, {
      method: "POST",
      credentials: "include", // 必须，发送 httpOnly cookie
    });
    if (!resp.ok) {
      setAccessToken(null);
      return false;
    }
    const data = (await resp.json()) as TokenResponse;
    setAccessToken(data.access_token);
    return true;
  } catch (err) {
    console.error("refresh failed", err);
    setAccessToken(null);
    return false;
  }
}

// 登录流程：POST /api/register 返回 access_token（body），后端会 Set-Cookie refresh_token (httpOnly)
async function doRegister(e: Event) {
  e.preventDefault();
  const username = (document.getElementById("username") as HTMLInputElement).value.trim();
  const password = (document.getElementById("password") as HTMLInputElement).value;
  if (!username || !password) return alert("请输入用户名和密码");

  showPage("loading");
  try {
    const resp = await fetch(`${API_BASE}/api/register`, {
      method: "POST",
      credentials: "include", // 让浏览器接收后端 Set-Cookie（httpOnly）
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password } as LoginRequest),
    });
    if (!resp.ok) {
      const err = await resp.json().catch(() => null);
      alert(err?.detail || "登录失败");
      showPage("login");
      return;
    }
    const data = (await resp.json()) as TokenResponse;
    setAccessToken(data.access_token);
    showPage("home");
  } catch (err) {
    console.error(err);
    alert("网络错误");
    showPage("login");
  }
}

// 登录流程：POST /api/login 返回 access_token（body），后端会 Set-Cookie refresh_token (httpOnly)
async function doLogin(e: Event) {
  e.preventDefault();
  const username = (document.getElementById("username") as HTMLInputElement).value.trim();
  const password = (document.getElementById("password") as HTMLInputElement).value;
  if (!username || !password) return alert("请输入用户名和密码");

  showPage("loading");
  try {
    const resp = await fetch(`${API_BASE}/api/login`, {
      method: "POST",
      credentials: "include", // 让浏览器接收后端 Set-Cookie（httpOnly）
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password } as LoginRequest),
    });
    if (!resp.ok) {
      const err = await resp.json().catch(() => null);
      alert(err?.detail || "登录失败");
      showPage("login");
      return;
    }
    const data = (await resp.json()) as TokenResponse;
    setAccessToken(data.access_token);
    showPage("home");
  } catch (err) {
    console.error(err);
    alert("网络错误");
    showPage("login");
  }
}

// 查看用户信息：调用受保护的 /api/me（需要 Authorization header）
async function viewUserInfo() {
  showPage("loading");
  try {
    const resp = await apiFetch("/api/me", { method: "GET" });
    if (!resp.ok) {
      if (resp.status === 401) {
        alert("未授权，请重新登录");
        setAccessToken(null);
        showPage("login");
        return;
      }
      alert("获取信息失败");
      showPage("home");
      return;
    }
    const user = (await resp.json()) as UserOut;
    alert(`用户信息：\nID: ${user.id}\n用户名: ${user.username}`);
  } catch (err) {
    console.error(err);
    alert("请求失败");
  } finally {
    showPage(accessToken ? "home" : "login");
  }
}

// 登出：调用 /api/logout（后端会撤销 refresh token 并清 cookie）
async function doLogout() {
  showPage("loading");
  try {
    const resp = await fetch(`${API_BASE}/api/logout`, {
      method: "POST",
      credentials: "include",
    });
    // 不论后端响应如何，都清理前端状态
    setAccessToken(null);
    showPage("login");
    if (!resp.ok) {
      console.warn("logout response not ok", resp.status);
    }
  } catch (err) {
    console.error(err);
    setAccessToken(null);
    showPage("login");
  }
}

// 页面初始化：尝试通过 refresh 获取 access token（如果已有 httpOnly refresh cookie）
async function init() {
  showPage("loading");
  const refreshed = await tryRefresh();
  if (refreshed) {
    showPage("home");
  } else {
    showPage("login");
  }
}

// 事件绑定
registerForm.addEventListener("submit", doRegister); 
loginForm.addEventListener("submit", doLogin);          // loginFrom 登录后，会调用 doLogin 方法
btnInfo.addEventListener("click", viewUserInfo);
btnLogout.addEventListener("click", doLogout);

// 启动
init();