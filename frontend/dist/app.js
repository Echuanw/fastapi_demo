"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var API_BASE = "http://localhost:3000"; // 后端地址，按需修改
var accessToken = null; // 仅内存保存，避免 localStorage 的 XSS 风险
// UI 元素
var loginPage = document.getElementById("loginPage");
var homePage = document.getElementById("homePage");
var loadingDiv = document.getElementById("loading");
var welcomeP = document.getElementById("welcome");
var loginForm = document.getElementById("loginForm");
var btnInfo = document.getElementById("btnInfo");
var btnLogout = document.getElementById("btnLogout");
function showPage(id) {
    loginPage.classList.toggle("hidden", id !== "login");
    homePage.classList.toggle("hidden", id !== "home");
    loadingDiv.classList.toggle("hidden", id !== "loading");
}
function setAccessToken(token) {
    accessToken = token;
    if (token) {
        welcomeP.textContent = "已登录（access token 在内存中）";
    }
    else {
        welcomeP.textContent = "";
    }
}
// fetch wrapper：自动带 Authorization header；遇 401 尝试 refresh 并重试一次
function apiFetch(input_1) {
    return __awaiter(this, arguments, void 0, function (input, init, retry) {
        var headers, cfg, resp, refreshed;
        var _a;
        if (init === void 0) { init = {}; }
        if (retry === void 0) { retry = true; }
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    headers = new Headers(init.headers || {});
                    if (accessToken) {
                        headers.set("Authorization", "Bearer ".concat(accessToken));
                    }
                    cfg = __assign(__assign({}, init), { headers: headers, credentials: (_a = init.credentials) !== null && _a !== void 0 ? _a : "include" });
                    return [4 /*yield*/, fetch("".concat(API_BASE).concat(input), cfg)];
                case 1:
                    resp = _b.sent();
                    if (!(resp.status === 401 && retry)) return [3 /*break*/, 3];
                    return [4 /*yield*/, tryRefresh()];
                case 2:
                    refreshed = _b.sent();
                    if (refreshed) {
                        // 重试原请求一次（但不再无限重试）
                        return [2 /*return*/, apiFetch(input, init, false)];
                    }
                    _b.label = 3;
                case 3: return [2 /*return*/, resp];
            }
        });
    });
}
// 调用 /api/refresh，从 cookie 中读取 refresh token（httpOnly），并获取新的 access token
function tryRefresh() {
    return __awaiter(this, void 0, void 0, function () {
        var resp, data, err_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 3, , 4]);
                    return [4 /*yield*/, fetch("".concat(API_BASE, "/api/refresh"), {
                            method: "POST",
                            credentials: "include", // 必须，发送 httpOnly cookie
                        })];
                case 1:
                    resp = _a.sent();
                    if (!resp.ok) {
                        setAccessToken(null);
                        return [2 /*return*/, false];
                    }
                    return [4 /*yield*/, resp.json()];
                case 2:
                    data = (_a.sent());
                    setAccessToken(data.access_token);
                    return [2 /*return*/, true];
                case 3:
                    err_1 = _a.sent();
                    console.error("refresh failed", err_1);
                    setAccessToken(null);
                    return [2 /*return*/, false];
                case 4: return [2 /*return*/];
            }
        });
    });
}
// 登录流程：POST /api/login 返回 access_token（body），后端会 Set-Cookie refresh_token (httpOnly)
function doLogin(e) {
    return __awaiter(this, void 0, void 0, function () {
        var username, password, resp, err, data, err_2;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    e.preventDefault();
                    username = document.getElementById("username").value.trim();
                    password = document.getElementById("password").value;
                    if (!username || !password)
                        return [2 /*return*/, alert("请输入用户名和密码")];
                    showPage("loading");
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 6, , 7]);
                    return [4 /*yield*/, fetch("".concat(API_BASE, "/api/login"), {
                            method: "POST",
                            credentials: "include", // 让浏览器接收后端 Set-Cookie（httpOnly）
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ username: username, password: password }),
                        })];
                case 2:
                    resp = _a.sent();
                    if (!!resp.ok) return [3 /*break*/, 4];
                    return [4 /*yield*/, resp.json().catch(function () { return null; })];
                case 3:
                    err = _a.sent();
                    alert((err === null || err === void 0 ? void 0 : err.detail) || "登录失败");
                    showPage("login");
                    return [2 /*return*/];
                case 4: return [4 /*yield*/, resp.json()];
                case 5:
                    data = (_a.sent());
                    setAccessToken(data.access_token);
                    showPage("home");
                    return [3 /*break*/, 7];
                case 6:
                    err_2 = _a.sent();
                    console.error(err_2);
                    alert("网络错误");
                    showPage("login");
                    return [3 /*break*/, 7];
                case 7: return [2 /*return*/];
            }
        });
    });
}
// 查看用户信息：调用受保护的 /api/me（需要 Authorization header）
function viewUserInfo() {
    return __awaiter(this, void 0, void 0, function () {
        var resp, user, err_3;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    showPage("loading");
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 4, 5, 6]);
                    return [4 /*yield*/, apiFetch("/api/me", { method: "GET" })];
                case 2:
                    resp = _a.sent();
                    if (!resp.ok) {
                        if (resp.status === 401) {
                            alert("未授权，请重新登录");
                            setAccessToken(null);
                            showPage("login");
                            return [2 /*return*/];
                        }
                        alert("获取信息失败");
                        showPage("home");
                        return [2 /*return*/];
                    }
                    return [4 /*yield*/, resp.json()];
                case 3:
                    user = (_a.sent());
                    alert("\u7528\u6237\u4FE1\u606F\uFF1A\nID: ".concat(user.id, "\n\u7528\u6237\u540D: ").concat(user.username));
                    return [3 /*break*/, 6];
                case 4:
                    err_3 = _a.sent();
                    console.error(err_3);
                    alert("请求失败");
                    return [3 /*break*/, 6];
                case 5:
                    showPage(accessToken ? "home" : "login");
                    return [7 /*endfinally*/];
                case 6: return [2 /*return*/];
            }
        });
    });
}
// 登出：调用 /api/logout（后端会撤销 refresh token 并清 cookie）
function doLogout() {
    return __awaiter(this, void 0, void 0, function () {
        var resp, err_4;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    showPage("loading");
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, fetch("".concat(API_BASE, "/api/logout"), {
                            method: "POST",
                            credentials: "include",
                        })];
                case 2:
                    resp = _a.sent();
                    // 不论后端响应如何，都清理前端状态
                    setAccessToken(null);
                    showPage("login");
                    if (!resp.ok) {
                        console.warn("logout response not ok", resp.status);
                    }
                    return [3 /*break*/, 4];
                case 3:
                    err_4 = _a.sent();
                    console.error(err_4);
                    setAccessToken(null);
                    showPage("login");
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    });
}
// 页面初始化：尝试通过 refresh 获取 access token（如果已有 httpOnly refresh cookie）
function init() {
    return __awaiter(this, void 0, void 0, function () {
        var refreshed;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    showPage("loading");
                    return [4 /*yield*/, tryRefresh()];
                case 1:
                    refreshed = _a.sent();
                    if (refreshed) {
                        showPage("home");
                    }
                    else {
                        showPage("login");
                    }
                    return [2 /*return*/];
            }
        });
    });
}
// 事件绑定
loginForm.addEventListener("submit", doLogin);
btnInfo.addEventListener("click", viewUserInfo);
btnLogout.addEventListener("click", doLogout);
// 启动
init();
