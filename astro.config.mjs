import { defineConfig } from 'astro/config'
import tailwind from "@astrojs/tailwind"

import robotsTxt from "astro-robots-txt"
const SERVER_PORT = 3000
const LOCALHOST_URL = `http://localhost:${SERVER_PORT}`
const LIVE_URL = `https://quochuyba.github.io`
const SCRIPT = process.env.npm_lifecycle_script || "";
const isBuilt = SCRIPT.includes("astro build");
let BASE_URL = LOCALHOST_URL; 
if (isBuilt) {
  BASE_URL = LIVE_URL;
}
export default defineConfig({
  server: {port: SERVER_PORT },
  site: BASE_URL,
  integrations: [
    tailwind({
      config: { applyBaseStyles: false },
    }),
    robotsTxt()
  ],
})
