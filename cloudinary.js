/**
 * cloudinary.js — Maarten Driessen Sporthorses
 *
 * Eén centraal bestand voor alle Cloudinary-functionaliteit:
 *   • upload widget openen (foto's, video's, drag&drop, Drive, Dropbox)
 *   • transformaties (thumbnail, hero, gallery, video poster)
 *   • config laden uit window.MD_CONFIG, of uit localStorage (Admin-instellingen)
 *   • upload-resultaat doorduwen naar Supabase (media-tabel)
 *
 * Gebruik:
 *   <script src="https://upload-widget.cloudinary.com/global/all.js"></script>
 *   <script src="cloudinary.js"></script>
 *   MDCloud.init({ cloudName: 'maartendriessen', uploadPreset: 'md_horses' });
 *   MDCloud.openUpload({ horseId: '...', onUploaded: (asset) => console.log(asset) });
 */

(function (global) {
  'use strict';

  const STORAGE_KEY = 'md.cl';

  const MDCloud = {
    config: {
      cloudName:    '',
      uploadPreset: '',
      folder:       'horses',
      // optioneel — voor Supabase persist
      supabase:     null
    },

    /* ---------------- INIT ---------------- */
    init(opts = {}) {
      // 1. opts > 2. window.MD_CONFIG > 3. localStorage
      const fromGlobal  = (global.MD_CONFIG && global.MD_CONFIG.cloudinary) || {};
      const fromStorage = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
      this.config = Object.assign({}, this.config, fromStorage, fromGlobal, opts);

      if (opts.supabase) this.config.supabase = opts.supabase;

      // Persist (handig na invullen in Admin Instellingen)
      if (opts.cloudName || opts.uploadPreset) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
          cloudName:    this.config.cloudName,
          uploadPreset: this.config.uploadPreset,
          folder:       this.config.folder
        }));
      }
      return this;
    },

    isReady() {
      return !!(this.config.cloudName && this.config.uploadPreset);
    },

    /* ---------------- URL BUILDERS ---------------- */
    /**
     * Bouw een Cloudinary-URL met transformaties.
     *   MDCloud.url('horses/rubel_abc123', { w:800, h:1000, c:'fill', g:'auto', q:'auto', f:'auto' })
     */
    url(publicId, opts = {}) {
      if (!publicId) return '';
      if (publicId.startsWith('http')) return publicId; // al volledige URL
      const c = this.config.cloudName;
      if (!c) return publicId;
      const parts = [];
      const map = { w:'w', h:'h', c:'c', g:'g', q:'q', f:'f', r:'r', e:'e', dpr:'dpr', ar:'ar' };
      Object.entries(opts).forEach(([k, v]) => {
        if (map[k] && v !== undefined && v !== null) parts.push(`${map[k]}_${v}`);
      });
      const tx = parts.length ? parts.join(',') + '/' : '';
      const type = opts.resourceType === 'video' ? 'video' : 'image';
      return `https://res.cloudinary.com/${c}/${type}/upload/${tx}${publicId}`;
    },

    // Klaargemaakte transformaties voor de site
    thumb (id) { return this.url(id, { w:480,  h:600, c:'fill', g:'auto', q:'auto', f:'auto' }); },
    hero  (id) { return this.url(id, { w:1600, h:900, c:'fill', g:'auto', q:'auto', f:'auto' }); },
    card  (id) { return this.url(id, { w:800,  h:1000,c:'fill', g:'auto', q:'auto', f:'auto' }); },
    cover (id) { return this.url(id, { w:1200, h:800, c:'fill', g:'auto', q:'auto', f:'auto' }); },
    avatar(id) { return this.url(id, { w:120,  h:120, c:'fill', g:'face', q:'auto', f:'auto', r:'max' }); },
    poster(id) { return this.url(id, { w:1200, h:675, c:'fill', q:'auto', f:'jpg', resourceType:'video' }); },

    /* ---------------- UPLOAD WIDGET ---------------- */
    /**
     * Open de Cloudinary Upload Widget.
     * @param {Object} opts
     * @param {string} opts.horseId       — link asset(s) naar een paard
     * @param {string} opts.newsId        — of aan een news-post
     * @param {string} opts.referenceId   — of aan een referentie
     * @param {string} opts.folder        — override folder (default: config.folder)
     * @param {boolean} opts.multiple     — meerdere bestanden tegelijk (default: true)
     * @param {Function} opts.onUploaded  — callback per geüploade asset
     * @param {Function} opts.onClose     — callback bij sluiten widget
     */
    openUpload(opts = {}) {
      if (!this.isReady())  { alert('Cloudinary niet geconfigureerd. Vul cloud name & upload preset in onder Admin → Instellingen.'); return; }
      if (!global.cloudinary) { alert('Cloudinary widget script niet geladen.'); return; }

      const folder = opts.folder || this.config.folder || 'horses';
      const widget = global.cloudinary.createUploadWidget({
        cloudName:    this.config.cloudName,
        uploadPreset: this.config.uploadPreset,
        folder,
        multiple:     opts.multiple !== false,
        maxFiles:     opts.maxFiles || 30,
        sources:      ['local','url','camera','dropbox','google_drive','image_search'],
        resourceType: 'auto',
        clientAllowedFormats: ['jpg','jpeg','png','webp','heic','mp4','mov','m4v'],
        maxImageFileSize: 20_000_000,
        maxVideoFileSize: 200_000_000,
        showAdvancedOptions: true,
        cropping:      false,
        styles: {
          palette: {
            window:       '#FAF7F2',
            sourceBg:     '#FBF8F2',
            windowBorder: '#E4DCCC',
            tabIcon:      '#0A0A0A',
            inactiveTabIcon: '#7A7068',
            menuIcons:    '#0A0A0A',
            link:         '#8B7355',
            action:       '#0A0A0A',
            inProgress:   '#8B7355',
            complete:     '#4F8A5E',
            error:        '#A83A3A',
            textDark:     '#0A0A0A',
            textLight:    '#FFFFFF'
          },
          fonts: {
            default: { active: true }
          }
        },
        context: {
          horse_id:     opts.horseId     || '',
          news_id:      opts.newsId      || '',
          reference_id: opts.referenceId || ''
        }
      }, (err, res) => {
        if (err) { console.error('Cloudinary error', err); return; }
        if (!res || !res.event) return;

        if (res.event === 'success') {
          const a = this._normalizeAsset(res.info);
          if (typeof opts.onUploaded === 'function') opts.onUploaded(a);
          this._persist(a, { horseId: opts.horseId, newsId: opts.newsId, referenceId: opts.referenceId });
        }
        if (res.event === 'close' && typeof opts.onClose === 'function') opts.onClose();
      });
      widget.open();
      return widget;
    },

    _normalizeAsset(info) {
      return {
        public_id:     info.public_id,
        secure_url:    info.secure_url,
        resource_type: info.resource_type,             // image | video | raw
        format:        info.format,
        width:         info.width  || null,
        height:        info.height || null,
        bytes:         info.bytes  || null,
        duration:      info.duration || null,
        original_filename: info.original_filename || ''
      };
    },

    /**
     * Schrijft de geüploade asset naar Supabase (tabel `media`).
     * Wordt automatisch overgeslagen als er geen Supabase-client geregistreerd is.
     */
    async _persist(asset, links = {}) {
      const sb = this.config.supabase;
      if (!sb) return; // geen Supabase → klaar
      try {
        const row = {
          horse_id:     links.horseId     || null,
          news_id:      links.newsId      || null,
          reference_id: links.referenceId || null,
          public_id:    asset.public_id,
          secure_url:   asset.secure_url,
          resource_type:asset.resource_type,
          format:       asset.format,
          width:        asset.width,
          height:       asset.height,
          bytes:        asset.bytes,
          duration_sec: asset.duration,
          position:     0
        };
        const { error } = await sb.from('media').insert(row);
        if (error) console.warn('Supabase media insert:', error.message);

        // Als er nog geen cover op het paard staat → zet deze als cover
        if (links.horseId) {
          const { data: cur } = await sb.from('horses').select('cover_url').eq('id', links.horseId).single();
          if (cur && !cur.cover_url) {
            await sb.from('horses').update({
              cover_url:       asset.secure_url,
              cover_public_id: asset.public_id
            }).eq('id', links.horseId);
          }
        }
      } catch (e) {
        console.warn('Supabase persist failed', e);
      }
    },

    /* ---------------- HELPERS ---------------- */
    /** Maak een unsigned-upload via direct POST (zonder widget — handig voor bulk imports). */
    async uploadFile(file, opts = {}) {
      if (!this.isReady()) throw new Error('Cloudinary niet geconfigureerd');
      const fd = new FormData();
      fd.append('file', file);
      fd.append('upload_preset', this.config.uploadPreset);
      fd.append('folder', opts.folder || this.config.folder || 'horses');
      const res = await fetch(`https://api.cloudinary.com/v1_1/${this.config.cloudName}/auto/upload`, {
        method: 'POST', body: fd
      });
      if (!res.ok) throw new Error('Upload mislukt: ' + res.status);
      return this._normalizeAsset(await res.json());
    },

    /** Importeer een externe URL (bv. de huidige maartendriessen.be foto's) direct in Cloudinary. */
    async importUrl(url, opts = {}) {
      if (!this.isReady()) throw new Error('Cloudinary niet geconfigureerd');
      const fd = new FormData();
      fd.append('file', url);
      fd.append('upload_preset', this.config.uploadPreset);
      fd.append('folder', opts.folder || this.config.folder || 'horses');
      const res = await fetch(`https://api.cloudinary.com/v1_1/${this.config.cloudName}/image/upload`, {
        method: 'POST', body: fd
      });
      if (!res.ok) throw new Error('Import mislukt: ' + res.status);
      return this._normalizeAsset(await res.json());
    }
  };

  global.MDCloud = MDCloud;

})(typeof window !== 'undefined' ? window : globalThis);
