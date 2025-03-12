def raqmhaqiqi(x):
    while True:
        try:
            return float(input(x))
        except ValueError:
            print("Error: dakhal chy raqm bhal nas aspipa7")

def jam3():
    numbers = []
   
    while True:
        a = raqmhaqiqi("ara chy raqm oder schreiben Sie einfach Null ")
        if a == 0:
            break
        numbers.append(a)
    return sum(numbers)

def tar7():
    numbers = []
   
    while True:
        a = raqmhaqiqi("ara chy raqm oder schreiben Sie einfach Null ")
        if a == 0:
            break
        numbers.append(a)
    return numbers[0] - sum(numbers[1:])

def darb1(numbers):
    x = 1
    for num in numbers:
        x *= num
    return x
def darb():
    numbers = []
   
    while True:
        a = raqmhaqiqi("ara chy raqm oder schreiben Sie einfach Null ")
        if a == 0:
            break
        numbers.append(a)
    return darb1(numbers)

def qisma():
    while True:
        a = raqmhaqiqi("ara: ")
        b = raqmhaqiqi("ara: ")
        try:
            x = a / b
            return x
        except ZeroDivisionError:
            print("layomkin, mnghir 0")
        

def main():
    
    o = input("khtar, jam3, darb, qisma wla tar7(wla chy exit): ").lstrip().rstrip().lower()
    
    while True:
            if o == "exit":
                print("Bslama!")
                break

            if o not in ["jam3", "tar7", "darb", "qisma"]:
                o = input(("hadchi masalakchi choflk mn dkchi liqbel:  ")).lstrip().rstrip().lower()
                continue

        
            if o == "jam3":
                print("result ", jam3())
            elif o == "tar7":
                print("result ", tar7())
            elif o == "darb":
                print("result ", darb())
            else:
                o == "qisma"
                print(qisma())

            o = input("khtar, jam3, darb, qisma wla tar7(wla chy exit): ")

main()
