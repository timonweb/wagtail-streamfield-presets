import wagtailConfig from '@wagtail/eslint-config-wagtail';

export default [
  { ignores: ['.venv/**', 'demo/**', 'node_modules/**', 'htmlcov/**'] },
  ...wagtailConfig,
  {
    files: ['src/**/static/**/*.js'],
    // Served as-is to the Wagtail admin, which provides these as globals.
    languageOptions: {
      sourceType: 'script',
      globals: { window: 'readonly', document: 'readonly' },
    },
  },
];
