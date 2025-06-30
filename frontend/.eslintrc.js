module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    'plugin:vue/essential',
    'eslint:recommended'
  ],
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false,
    ecmaVersion: 2020
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'vue/no-unused-components': 'warn',
    'no-unused-vars': 'warn',
    'vue/multi-word-component-names': ['error', {
      ignores: ['Layout', 'Dashboard', 'Login', 'Register', 'Models', 'Breadcrumb']
    }]
  },
  overrides: [
    {
      files: ['*.vue'],
      parser: 'vue-eslint-parser'
    }
  ]
} 