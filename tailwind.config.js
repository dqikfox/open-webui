import typography from '@tailwindcss/typography';
import containerQuries from '@tailwindcss/container-queries';

/** @type {import('tailwindcss').Config} */
export default {
	darkMode: 'class',
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				gray: {
					50: 'var(--color-gray-50, #1a0a0a)',
					100: 'var(--color-gray-100, #1f0f0f)',
					200: 'var(--color-gray-200, #2a1515)',
					300: 'var(--color-gray-300, #3d1f1f)',
					400: 'var(--color-gray-400, #4d2626)',
					500: 'var(--color-gray-500, #5c2e2e)',
					600: 'var(--color-gray-600, #7a3838)',
					700: 'var(--color-gray-700, #8f4444)',
					800: 'var(--color-gray-800, #1a1a1a)',
					850: 'var(--color-gray-850, #0f0f0f)',
					900: 'var(--color-gray-900, #0a0a0a)',
					950: 'var(--color-gray-950, #050505)'
				},
				ultron: {
					red: '#ff0000',
					'red-glow': '#ff3333',
					'red-dark': '#cc0000',
					'red-bright': '#ff6666',
					dark: '#0a0a0a',
					darker: '#050505'
				}
			},
			typography: {
				DEFAULT: {
					css: {
						pre: false,
						code: false,
						'pre code': false,
						'code::before': false,
						'code::after': false
					}
				}
			},
			padding: {
				'safe-bottom': 'env(safe-area-inset-bottom)'
			}
		}
	},
	plugins: [typography, containerQuries]
};
