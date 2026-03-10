// TypeScript 不认识 .vue 文件导致 main.ts 中出现类型报错。
// 添加这个 .d.ts 类型声明文件
declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}