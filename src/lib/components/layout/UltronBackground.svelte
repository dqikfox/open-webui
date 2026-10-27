<script>
	import { onMount } from 'svelte';
	
	let canvas;
	let ctx;
	let particles = [];
	let circuits = [];
	
	class Particle {
		constructor(x, y) {
			this.x = x;
			this.y = y;
			this.vx = (Math.random() - 0.5) * 0.5;
			this.vy = (Math.random() - 0.5) * 0.5;
			this.radius = Math.random() * 2 + 1;
			this.opacity = Math.random() * 0.5 + 0.3;
		}
		
		update() {
			this.x += this.vx;
			this.y += this.vy;
			
			if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
			if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
		}
		
		draw() {
			ctx.beginPath();
			ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
			ctx.fillStyle = `rgba(255, 0, 0, ${this.opacity})`;
			ctx.shadowBlur = 10;
			ctx.shadowColor = 'rgba(255, 0, 0, 0.8)';
			ctx.fill();
			ctx.shadowBlur = 0;
		}
	}
	
	class Circuit {
		constructor() {
			this.reset();
		}
		
		reset() {
			this.x1 = Math.random() * canvas.width;
			this.y1 = Math.random() * canvas.height;
			this.x2 = this.x1 + (Math.random() - 0.5) * 200;
			this.y2 = this.y1 + (Math.random() - 0.5) * 200;
			this.progress = 0;
			this.speed = Math.random() * 0.02 + 0.01;
			this.opacity = Math.random() * 0.3 + 0.2;
		}
		
		update() {
			this.progress += this.speed;
			if (this.progress >= 1) {
				this.reset();
			}
		}
		
		draw() {
			const x = this.x1 + (this.x2 - this.x1) * this.progress;
			const y = this.y1 + (this.y2 - this.y1) * this.progress;
			
			ctx.beginPath();
			ctx.moveTo(this.x1, this.y1);
			ctx.lineTo(x, y);
			ctx.strokeStyle = `rgba(255, 0, 0, ${this.opacity})`;
			ctx.lineWidth = 2;
			ctx.shadowBlur = 15;
			ctx.shadowColor = 'rgba(255, 0, 0, 0.6)';
			ctx.stroke();
			ctx.shadowBlur = 0;
			
			// Draw glowing point at current position
			ctx.beginPath();
			ctx.arc(x, y, 4, 0, Math.PI * 2);
			ctx.fillStyle = `rgba(255, 51, 51, ${this.opacity + 0.3})`;
			ctx.shadowBlur = 20;
			ctx.shadowColor = 'rgba(255, 0, 0, 1)';
			ctx.fill();
			ctx.shadowBlur = 0;
		}
	}
	
	function animate() {
		ctx.fillStyle = 'rgba(10, 10, 10, 0.1)';
		ctx.fillRect(0, 0, canvas.width, canvas.height);
		
		particles.forEach(particle => {
			particle.update();
			particle.draw();
		});
		
		circuits.forEach(circuit => {
			circuit.update();
			circuit.draw();
		});
		
		// Draw connections between nearby particles
		for (let i = 0; i < particles.length; i++) {
			for (let j = i + 1; j < particles.length; j++) {
				const dx = particles[i].x - particles[j].x;
				const dy = particles[i].y - particles[j].y;
				const distance = Math.sqrt(dx * dx + dy * dy);
				
				if (distance < 150) {
					ctx.beginPath();
					ctx.moveTo(particles[i].x, particles[i].y);
					ctx.lineTo(particles[j].x, particles[j].y);
					ctx.strokeStyle = `rgba(255, 0, 0, ${0.2 * (1 - distance / 150)})`;
					ctx.lineWidth = 1;
					ctx.stroke();
				}
			}
		}
		
		requestAnimationFrame(animate);
	}
	
	onMount(() => {
		ctx = canvas.getContext('2d');
		canvas.width = window.innerWidth;
		canvas.height = window.innerHeight;
		
		// Create particles
		for (let i = 0; i < 50; i++) {
			particles.push(new Particle(
				Math.random() * canvas.width,
				Math.random() * canvas.height
			));
		}
		
		// Create circuits
		for (let i = 0; i < 20; i++) {
			circuits.push(new Circuit());
		}
		
		animate();
		
		const handleResize = () => {
			canvas.width = window.innerWidth;
			canvas.height = window.innerHeight;
		};
		
		window.addEventListener('resize', handleResize);
		
		return () => {
			window.removeEventListener('resize', handleResize);
		};
	});
</script>

<canvas
	bind:this={canvas}
	class="fixed top-0 left-0 w-full h-full pointer-events-none z-0"
	style="background: linear-gradient(135deg, #0a0a0a 0%, #1a0a0a 50%, #0a0a0a 100%);"
/>

<style>
	canvas {
		opacity: 0.6;
	}
</style>
