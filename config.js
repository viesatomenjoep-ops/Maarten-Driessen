/**
 * config.js — globale configuratie voor index.html / admin.html
 *
 * Eén plek waar je je keys neerzet. Wordt automatisch opgepikt door
 * cloudinary.js en het Supabase-stuk in admin.html.
 *
 * Plaats in dezelfde map als de HTML-bestanden en zorg dat je
 * <script src="config.js"></script> laadt vóór de andere scripts.
 */

window.MD_CONFIG = {
  // ---------------------------------------------------------------
  //  SUPABASE — managed (https://supabase.com → Settings → API)
  // ---------------------------------------------------------------
  supabase: {
    url:        '',  // https://xxxxxxxxxxxx.supabase.co
    anonKey:    '',  // eyJhbGciOi...
    schema:     'public'
  },

  // ---------------------------------------------------------------
  //  CLOUDINARY (dashboard.cloudinary.com → Account details)
  // ---------------------------------------------------------------
  cloudinary: {
    cloudName:    '',          // bv. 'maartendriessen'
    uploadPreset: '',          // unsigned preset, bv. 'md_horses'
    folder:       'horses'
  },

  // ---------------------------------------------------------------
  //  LOKAAL — als je liever de Docker-stack gebruikt:
  //  zet hierboven URL = 'http://localhost:3000' (PostgREST)
  //  en laat anonKey leeg.
  // ---------------------------------------------------------------

  site: {
    defaultLocale: 'nl',
    locales:       ['nl','en','fr','de']
  }
};
