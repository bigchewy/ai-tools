# daily-signal Plugin

Morning and evening check-in rituals for self-awareness and personal growth.

## Commands

### `/morning-signal`
General morning reflection guided by expert psychologists.

### `/morning-signal-hoffman-only`
Hoffman Quadrinity check-in guided by Diana Chapman, focusing on:
- 🧠 Head - What am I thinking?
- ❤️ Heart - What am I feeling emotionally?
- 🚶 Body - What sensations are present in my body?
- ✨ Spirit - What does my Spiritual Self want me to know?

### `/evening-signal`
Evening reflection and gratitude practice.

## Resources

This plugin includes profiles for six psychologists who guide the check-ins:
- **Diana Chapman** - Conscious Leadership, Hoffman Quadrinity
- **Brené Brown** - Vulnerability, shame resilience
- **Jim Loehr** - Energy management, performance psychology
- **Marsha Linehan** - DBT, emotional regulation
- **Martin Seligman** - Positive psychology, learned optimism
- **Steven Hayes** - ACT, psychological flexibility

## Configuration

The plugin looks for your personal profile in this order:
1. `virtual_board/profile/main_profile.md`
2. `profile/main_profile.md`
3. `daily-signal-profile.md`

If you don't have a profile, create one using `resources/profile-template.md` as a starting point.

## File Storage

Check-ins are saved to:
- Morning: `domains/check_ins/morning/YYYY-MM-DD.md`
- Evening: `domains/check_ins/evening/YYYY-MM-DD.md`

Make sure these directories exist in your vault, or the plugin will create them.

## Tips

- Use the Hoffman check-in when you need deep self-inquiry
- Use the general morning signal for quicker daily reflection
- Evening signals work best as wind-down rituals
- Psychologists adapt to your Enneagram type if specified in your profile
