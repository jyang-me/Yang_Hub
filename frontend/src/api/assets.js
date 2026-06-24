const localApiOrigin = 'http://127.0.0.1:8000'

export function getAssetUrl(path) {
  if (!path) {
    return ''
  }

  if (/^https?:\/\//i.test(path)) {
    return path
  }

  const normalizedPath = path.startsWith('/') ? path : `/${path}`

  if (import.meta.env.PROD) {
    return normalizedPath
  }

  return `${localApiOrigin}${normalizedPath}`
}
