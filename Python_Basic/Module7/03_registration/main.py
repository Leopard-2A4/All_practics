# TODO здесь писать код
def validate_registration(line):
    parts = line.strip().split()
    if len(parts) != 3:
        raise IndexError("НЕ присутствуют все три поля")
    name, email, age = parts
    if not name.isalpha():
        raise NameError("Поле «Имя» содержит НЕ только буквы")

    if '@' not in email or '.' not in email:
        raise SyntaxError("Поле «Имейл» НЕ содержит @ и точку")

    try:
        age = int(age)
        if not (10 <= age <= 99):
            raise ValueError("Поле «Возраст» НЕ представляет число от 10 до 99")
    except ValueError as e:
        raise ValueError("Поле «Возраст» НЕ представляет число от 10 до 99")

def main():
    with open('registrations.txt', 'r', encoding='utf-8') as file, \
            open('registrations_good.log', 'w', encoding='utf-8') as good_log, \
            open('registrations_bad.log', 'w', encoding='utf-8') as bad_log:

        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                validate_registration(line)
                good_log.write(line + '\n')
            except (IndexError, NameError, SyntaxError, ValueError) as exception:
                bad_log.write(f"{line}\t{exception}\n")


main()