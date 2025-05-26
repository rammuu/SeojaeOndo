import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: null,
    username: null
  }),
  actions: {
    setToken(token) {
      this.token = token
    },
    setUsername(username) {
      this.username = username
    },
    logout() {
      this.token = null
      this.username = null
      localStorage.removeItem('authToken')
    },
    setUser(data) {
      this.user = data
    },
    clearUser() {
      this.user = null
    },
  }
})
