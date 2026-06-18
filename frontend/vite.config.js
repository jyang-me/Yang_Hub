import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

function utf8ResponseHeaders() {
  return {
    name: 'utf8-response-headers',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const setHeader = res.setHeader.bind(res)

        res.setHeader = (name, value) => {
          if (
            String(name).toLowerCase() === 'content-type' &&
            typeof value === 'string' &&
            !value.toLowerCase().includes('charset') &&
            /^(text\/html|text\/css|text\/javascript|application\/javascript)/i.test(value)
          ) {
            return setHeader(name, `${value}; charset=utf-8`)
          }

          return setHeader(name, value)
        }

        next()
      })
    },
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss(), utf8ResponseHeaders()],
})
