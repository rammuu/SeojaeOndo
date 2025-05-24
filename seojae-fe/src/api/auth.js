import api from './axios'

export function registerUser(payload) {
  return api.post('auth/registration/', payload)
}


export function checkUsername(username) {
  return api.get('auth/check-username/', {
    params: { username }
  })
}

export function checkNickname(nickname) {
  return api.get('auth/check-nickname/', {
    params: { nickname }
  })
}