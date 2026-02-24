# 🚀 Galaxy Ship — Feature TODO

## 🟢 Low Effort

- [ ] **Score milestones / speed tiers** — Flash text like *"SPEED UP!"* or *"🔥 50 POINTS!"* every N points. Label + `Clock.schedule_once` to hide it. (`main.py` update loop + `galaxy.kv`)
- [ ] **Screen shake on game over** — Offset `perspective_point_x/y` by a small random amount for ~0.3s before showing game over. (`game_manager.py` → `game_over()`)
- [ ] **Tween/animate the score counter** — Use Kivy `Animation` to smoothly count up the score instead of instant jumps. (`galaxy.kv` score label)
- [ ] **"NEW HIGH SCORE! 🏆" on game over** — Show indicator text when the player beats their record. (`game_manager.py` → `game_over()` + `restart.kv`)
- [ ] **Particle trail behind ship** — Spawn small fading dots/quads behind the ship each frame using a list of recent positions. (`ship.py`)

## 🟡 Medium Effort

- [ ] **Collectible stars/coins on tiles** — Random items on tiles; collecting adds bonus score. Render as small colored quads, collision check like ship-tile. (New `collectibles.py` + `land_tiles.py` + `main.py`)
- [ ] **Difficulty levels (Easy / Normal / Hard)** — Change starting `SPEED`, `v_l_spacing` decay rate, and `speed_x` per level. (`settings.py` + `settings.kv` + `game_manager.py`)
- [ ] **Animated starfield background** — Draw random small dots that slowly drift downward instead of static `bg1.jpg`. (New `starfield.py` or canvas drawing in `main.py`)
- [ ] **Ship invincibility flash on restart** — ~2s of invincibility where ship blinks (toggle alpha). Reduces frustration. (`ship.py` + `game_manager.py`)
- [ ] **Lives system (3 lives)** — Lose a life on collision instead of instant game over. Flash ship, keep going. Display hearts on HUD. (`game_manager.py` + `galaxy.kv` + `ship.py`)

## 🎨 Design / Polish

- [ ] **Glow effect on ship** — Draw a second, larger, semi-transparent triangle behind the ship for a neon glow look
- [ ] **Fade-in tiles** — New tiles far away start with low alpha, increasing as they approach for added depth
- [ ] **Pulsing title on menu** — Use `Animation` to gently scale "GALAXY SHIP" title up/down on menu screen
- [ ] **Color theme unlocks** — Lock some color presets behind score milestones (e.g., Gold unlocks at 100 pts) for progression