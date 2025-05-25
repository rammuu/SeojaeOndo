import api from './axios'

export function registerUser(payload) {
  return api.post('auth/registration/', payload)
}


export function checkUsernameAPI(username) {
  return api.get('auth/check-username/', {
    params: { username }
  })
}

export function checkNicknameAPI(nickname) {
  return api.get('auth/check-nickname/', {
    params: { nickname }
  })
}

export function loginUser(data) {
  return api.post('auth/login/', data)
}