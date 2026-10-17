// Renders the raster images that live in public/ from their sources.
// Run with `npm run images` after changing the logo, the favicon or the spring
// meetup photo, then commit the results.
//
//   public/og-image.jpg            1200×630 preview shown when the site is shared (Discord, WhatsApp…)
//   public/logo-512.png            the full logo as a PNG, for search engines' structured data
//   public/favicon.ico             16/32/48px tab icon for browsers and tools that ask for /favicon.ico
//   public/apple-touch-icon.png    180px home-screen icon for iPhones and iPads
//   public/icon-192.png, icon-512.png   home-screen icons for Android (listed in site.webmanifest)

import sharp from "sharp";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const root = (path) => fileURLToPath(new URL(`../${path}`, import.meta.url));

const logo = root("public/logo.svg");
const favicon = root("public/favicon.svg");
const photo = root("src/assets/photos/spring-meetup.jpg");
const RING_YELLOW = "#f3d038";

const render = (svg, size) => sharp(svg, { density: 600 }).resize(size, size).png();

// Full logo
await render(logo, 512).toFile(root("public/logo-512.png"));

// Share preview: the group photo cropped to 1200×630, keeping everyone's faces in
// frame, with the logo badge top-right over the sky and church tower (clear of faces).
const badge = await render(logo, 230).toBuffer();
const scaled = await sharp(photo).resize(1200).toBuffer(); // 1200×900
await sharp(scaled)
  .extract({ left: 0, top: 150, width: 1200, height: 630 })
  .composite([{ input: badge, top: 30, left: 1200 - 230 - 36 }])
  .jpeg({ quality: 82, mozjpeg: true })
  .toFile(root("public/og-image.jpg"));

// Home-screen icons. Phones crop these to their own shape (a rounded square or a
// circle), so the icon sits on a full-bleed yellow square with room around it.
const homeScreenIcon = async (size, file) => {
  const inner = Math.round(size * 0.84);
  const icon = await render(favicon, inner).toBuffer();
  await sharp({ create: { width: size, height: size, channels: 4, background: RING_YELLOW } })
    .composite([{ input: icon, gravity: "centre" }])
    .png()
    .toFile(root(`public/${file}`));
};
await homeScreenIcon(180, "apple-touch-icon.png");
await homeScreenIcon(192, "icon-192.png");
await homeScreenIcon(512, "icon-512.png");

// favicon.ico: an ICO file is a small header followed by PNG images.
const icoSizes = [16, 32, 48];
const pngs = await Promise.all(icoSizes.map((size) => render(favicon, size).toBuffer()));
const header = Buffer.alloc(6 + 16 * pngs.length);
header.writeUInt16LE(0, 0); // reserved
header.writeUInt16LE(1, 2); // type: icon
header.writeUInt16LE(pngs.length, 4);
let offset = header.length;
pngs.forEach((png, i) => {
  const entry = 6 + 16 * i;
  header.writeUInt8(icoSizes[i], entry); // width
  header.writeUInt8(icoSizes[i], entry + 1); // height
  header.writeUInt16LE(1, entry + 4); // colour planes
  header.writeUInt16LE(32, entry + 6); // bits per pixel
  header.writeUInt32LE(png.length, entry + 8);
  header.writeUInt32LE(offset, entry + 12);
  offset += png.length;
});
await writeFile(root("public/favicon.ico"), Buffer.concat([header, ...pngs]));

console.log("Wrote og-image.jpg, logo-512.png, favicon.ico and the home-screen icons in public/");
