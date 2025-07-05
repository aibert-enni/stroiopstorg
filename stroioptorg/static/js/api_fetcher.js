async function customFetchWithRefresh(url, options = {}, retry = true) {
  options.credentials = 'include';  // Чтобы всегда шли куки

  let response = await fetch(url, options);

  if (response.status === 401 && retry) {
    // Пробуем рефрешнуть
    const refreshResponse = await fetch('/api/v1/auth/token/refresh/', {
      method: 'POST',
      credentials: 'include'
    });

    if (refreshResponse.ok) {
      // После успешного refresh, повторяем оригинальный запрос
      response = await customFetchWithRefresh(url, options, false);
    } else {
      console.error('Refresh failed. Redirecting to login...');
      // Здесь можно редиректить на login
    }
  }

  return response;
}

async function api(url, options = {}) {
  const response = await customFetchWithRefresh(url, options);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error ${response.status}`);
  }

  return response;
}