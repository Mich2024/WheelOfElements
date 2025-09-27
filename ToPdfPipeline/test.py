
template_line = open('Template_Line_Mod.txt', 'r')
template_race = open('Template_Race_Single.txt', 'r')
template_boilerplate = open('Template_Boilerplate.txt', 'r')

lines = template_race.read()

lines = lines.replace(r"${Mods}", "Butter")

print(repr(lines))




