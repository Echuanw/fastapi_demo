import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    tokenType: '',
    accessToken: ''
  }),
  actions: {
    setAccessToken(tokenType:string, token:string) {
      this.tokenType = tokenType
      this.accessToken = token
    },
    clearAccessToken() {
      this.tokenType = ''
      this.accessToken = ''
    }
  }
})