# ðŸ"° BizNews Article Generator

Skrip otomatis untuk generate artikel dari Google Sheets dan mengintegrasikannya **langsung** ke website BizNews (menu News, Search, Related Articles).

## âœ¨ Fitur

- âœ… Baca data dari Google Sheets (via Apps Script JSON endpoint)
- âœ… **Otomatis update `articles.json`** (database pusat website)
- âœ… Generate file HTML artikel terintegrasi ke folder `article/`
- âœ… File HTML match styling & layout website yang sudah ada
- âœ… Support gambar lokal atau URL publik
- âœ… Otomatis muncul di **menu News**, **Search**, & **Related Articles**
- âœ… Slug otomatis dari judul atau kolom `slug`
- âœ… Backup otomatis `articles.json` sebelum update

## ðŸ"‹ Persyaratan

- **Node.js 14+** (download dari https://nodejs.org)
- **Google Sheets** dengan data artikel terstruktur
- **Apps Script endpoint** sudah di-deploy (berisi URL: https://script.google.com/macros/s/AKfycbzk7H09i-P5_5wPc82mgr53poH-3wtJi8kEe3eIsTqHmcdutsT-T1sPgnA5qx1SLtzpSg/exec)
- **Folder `img/`** untuk menyimpan gambar artikel

## ðŸš€ Quick Start

### 1. Pastikan Dependencies Terinstall

Jika belum, jalankan di folder `tools/`:
```bash
npm install
```

### 2. Verifikasi Config

URL endpoint Google Sheets sudah benar di `generate.js`:
```javascript
const SHEETS_URL = 'https://script.google.com/macros/s/AKfycbzk7H09i-P5_5wPc82mgr53poH-3wtJi8kEe3eIsTqHmcdutsT-T1sPgnA5qx1SLtzpSg/exec';
```

### 3. Jalankan Generator

```bash
npm start
```

atau:
```bash
node generate.js
```

**Output:**
- âœ… Artikel HTML baru di `article/` folder
- âœ… `articles.json` di-update dengan entry baru
- âœ… Backup otomatis: `articles.json.bak.xxxxx`
- âœ… Artikel otomatis muncul di `news.html` dan `search.html`

**Testing:**
1. Buka `news.html` â†' artikel terbaru akan di-list paling atas
2. Buka `search.html` â†' cari artikelberdasarkan judul atau kategori
3. Klik artikel â†' buka file HTML di `article/berita1-f.html` (atau nama slug Anda)

## ðŸ"Š Format Google Sheet

**Kolom minimal yang diperlukan:**

| slug | title | date | category | badge | image | excerpt | content | author |
|------|-------|------|----------|-------|-------|---------|---------|--------|
| berita1-f | Perhutani KPH... | 2026-02-02 | Lingkungan | Utama | beritaf1.jpg | Ringkasan... | `<p>Isi...</p>` | Alfin S. |

**Keterangan:**
- `slug`: ID unik artikel (nama file), lowercase, gunakan `-` bukan spasi. **Bisa kosong** â† akan auto-generate dari `title`.
- `title`: Judul artikel **(wajib)**.
- `date`: Format YYYY-MM-DD **(wajib)**. Atau format lokal: "02-Feb-2026", "Feb 2, 2026", dll.
- `category`: Kategori artikel (Lingkungan, Teknologi, dll) - akan muncul di `articles.json` & filter search.
- `badge`: Label badge (Utama, Trending, Breaking, dll) - akan ditampilkan di artikel.
- `image`: Nama file gambar (mis. `beritaf1.jpg`) atau URL publik (mis. `https://...`).
  - **Jika nama file:** taruh file di folder `img/` â†' generator otomatis membuat path `img/beritaf1.jpg`.
  - **Jika URL:** pastikan bisa diakses publik.
- `excerpt`: Ringkasan artikel (akan ditampilkan di daftar berita di `news.html`).
- `content`: Isi artikel (bisa HTML atau plaintext). **Wajib** kalau excerpt kosong.
- `author`: Penulis (opsional).

## ðŸ-¼ï¸ Gambar

### Opsi 1: Local di Folder `img/` (Rekomendasi)
1. Upload gambar ke folder `img/` (misal: `img/beritaf1.jpg`).
2. Di Google Sheet, kolom `image` isi nama file: `beritaf1.jpg`
3. Generator otomatis membuat path: `../img/beritaf1.jpg`

### Opsi 2: URL Publik
1. Hosting gambar di server/CDN (atau Google Drive publik).
2. Di Google Sheet, kolom `image` isi URL lengkap: `https://example.com/foto1.jpg`
3. Generator menggunakan URL langsung.

**âš ï¸ Catatan:** Jika URL tidak accessible atau gambar terhapus, artikel akan tetap ditampilkan tapi tanpa gambar.

## ðŸ" Struktur & Alur Kerja

```
BizNews/
â"œâ"€â"€ article/                    â† Output file HTML artikel (terintegrasi)
â"œâ"€â"€ img/                        â† Simpan gambar di sini
â"œâ"€â"€ css/                        â† Stylesheet (shared dengan seluruh site)
â"œâ"€â"€ js/                         â† JavaScript
â"œâ"€â"€ articles.json               â† ðŸ"Š DATABASE PUSAT (di-update oleh generator)
â"œâ"€â"€ news.html                   â† ðŸ"° Daftar artikel (baca dari articles.json)
â"œâ"€â"€ search.html                 â† ðŸ" Search artikel (baca dari articles.json)
â"œâ"€â"€ index.html
â""â"€â"€ tools/
    â"œâ"€â"€ template-new.html       â† Template artikel (match layout website)
    â"œâ"€â"€ generate.js             â† ðŸ¤- Skrip generator utama
    â"œâ"€â"€ package.json
    â""â"€â"€ README.md               â† File ini
```

**Alur Kerja:**
1. **User** isi data berita di Google Sheets
2. **Generator** (node generate.js) baca dari Google Sheets
3. **Generator** membuat/update file HTML di `article/` folder
4. **Generator** update `articles.json` dengan entry baru
5. **news.html** & **search.html** otomatis menampilkan artikel baru (baca dari articles.json)
6. **Pengunjung** bisa baca artikel, lihat di news list, search, & lihat related articles

## âš™ï¸ Customization

### Update Template HTML

Jika ingin styling atau struktur berbeda, edit `template-new.html`. Variabel handlebars yang tersedia:
- `{{title}}` - Judul artikel
- `{{date}}` - Tanggal artikel
- `{{badge}}` - Label badge kategori
- `{{category}}` - Kategori artikel (untuk filtering)
- `{{{content}}}` - Isi artikel (raw HTML, 3 kurung = no-escape)
- `{{image}}` - Path/URL gambar
- `{{excerpt}}` - Ringkasan artikel
- `{{author}}` - Nama penulis
- `{{slug}}` - Slug artikel (ID unik)

### Update Google Sheets Endpoint

Jika URL endpoint berubah, update di `generate.js`:
```javascript
const SHEETS_URL = 'https://script.google.com/macros/s/NEW_ID/exec';
```

### Automasi / Scheduling (Optional)

Jalankan generator secara otomatis dengan:
1. **Windows Task Scheduler** - jalankan `node generate.js` setiap jam
2. **GitHub Actions** - trigger kala ada perubahan di repo
3. **Cron (Linux/Mac)** - `0 * * * * cd /path/to/tools && npm start`

### Update Format Tanggal

Jika format tanggal dari Sheets berbeda, modifikasi di `generate.js` baris yang parse `article.date`.

## ðŸ"§ Troubleshooting

### âŒ Error: "Template tidak ditemukan"
- âœ… Pastikan file `template-new.html` ada di folder `tools/`.
- âœ… Verifikasi path di `generate.js`: `const TEMPLATE_PATH = path.join(__dirname, 'template-new.html');`

### âŒ articles.json tidak update
- âœ… Pastikan path `articles.json` benar di `generate.js`.
- âœ… Pastikan file `articles.json` memiliki format JSON valid (bukan rusak).
- âœ… Lihat di terminal apakah ada error saat generate.

### âŒ Artikel tidak muncul di news.html atau search.html
- âœ… Cek `articles.json` - pastikan entry baru ada.
- âœ… Refresh browser (Ctrl+F5) untuk clear cache.
- âœ… Buka web browser console (F12) untuk lihat JavaScript error.
- âœ… Pastikan `news.html` & `search.html` punya JavaScript untuk load `articles.json`.

### âŒ Gambar tidak muncul
- âœ… **Jika lokal:** pastikan file gambar ada di folder `img/` dengan nama yang sama persis (case-sensitive di Linux/Mac).
- âœ… **Jika URL:** buka URL di browser untuk verifikasi akses & valid.
- âœ… Inspector (F12) â†' Network tab â†' lihat error saat load gambar.

### âŒ Slug tidak valid atau karakter aneh di filename
- âœ… Pastikan `title` atau `slug` di Sheet tidak ada karakter spesial yang berlebihan.
- âœ… Generator otomatis hapus karakter non-alphanumeric (kecuali `-` & space).

### âŒ Error "Data kosong atau format tidak valid"
- âœ… Buka endpoint Google Sheets di browser: https://script.google.com/macros/s/.../exec
- âœ… Pastikan mengembalikan JSON (bukan error atau HTML halaman).
- âœ… Cek sheet name di Apps Script: `getSheetByName('data')` harus sesuai nama sheet Anda.
- âœ… Pastikan baris pertama sheet adalah header & ada data di bawahnya.

### â„¹ï¸ Cara Lihat Hasil Generate
1. Jalankan: `npm start`
2. Buka file di `article/berita1-f.html` menggunakan Live Server atau buka langsung di browser.
3. Cek: navbar, footer, styling, konten, gambar, & related articles sidebar.
4. Verify di `news.html` â†' artikel muncul di list dengan gambar & excerpt.
5. Test search di `search.html` â†' cari judul artikel baru.

## ðŸ"š Referensi

- [Google Apps Script doGet()](https://developers.google.com/apps-script/guides/web/content)
- [Handlebars.js](https://handlebarsjs.com)
- [axios](https://github.com/axios/axios)

## ðŸ"ž Support

Jika ada pertanyaan atau masalah, hubungi tim development BizNews.

---

**Last updated:** February 12, 2026  
**Version:** 2.0 (articles.json integration)



