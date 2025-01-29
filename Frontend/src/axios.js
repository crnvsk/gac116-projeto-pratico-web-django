import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // Backend Django local
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false, // Desabilita envio de cookies para simplificação
});

// Flag para evitar loop infinito de refresh token
let isRefreshing = false;

// Adiciona automaticamente o token ao cabeçalho se ele existir no localStorage
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => Promise.reject(error));

// Interceptor para lidar com token expirado e tentar atualizar automaticamente
api.interceptors.response.use(
  (response) => response, // Retorna a resposta normal se não houver erro
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Flag para evitar loops infinitos

      try {
        const refreshToken = localStorage.getItem('refresh_token');

        if (!refreshToken || isRefreshing) {
          throw new Error('Sem refresh token disponível ou já em atualização.');
        }

        isRefreshing = true; // Bloqueia novas requisições de refresh enquanto a primeira não terminar

        // Requisição para renovar o token
        const { data } = await axios.post('/api/token/refresh/', {
          refresh: refreshToken,
        });

        // Salva o novo token
        localStorage.setItem('token', data.access);
        isRefreshing = false;

        // Atualiza o token na requisição original e tenta novamente
        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        return api(originalRequest);
      } catch (refreshError) {
        console.error('Erro ao renovar token:', refreshError);

        // Remove tokens inválidos e redireciona para login
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login'; // Redireciona para a página de login
      }
    }

    return Promise.reject(error);
  }
);

export default api;