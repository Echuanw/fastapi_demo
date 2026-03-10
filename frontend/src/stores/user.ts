import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token_type: '',
    accessToken: ''
  }),
  actions: {
    setAccessToken(token_type:string, token:string) {
      this.token_type = token_type
      this.accessToken = token
    },
    clearAccessToken() {
      this.token_type = ''
      this.accessToken = ''
    }
  }
})