# Effective Python [파이썬 코딩의 기술] - Ch 1 - Pythonic Way

해당 책은 다음의 링크에서 다운받을 수 있습니다 (영문) : [LINK](https://arisuchan.jp/λ/src/1498628824511-0.pdf)

> Effecive Python은 Python을 잘쓰기 위한 방법들을 소개하고 있다. 총 59가지이지만 흔히 아는 방법은 설명으로 적지 않았다. 그리고 비슷한 내용이지만 여러 파트에 나뉜 경우에 하나로 합쳐서 작성하기도 했다.

## Item 2. PEP 8 스타일 가이드를 따르자

Python Enhancement Proposal #8, 짧게 줄여서 [PEP 8](https://www.python.org/dev/peps/pep-0008/), 라는 것이 있는데 이는 Python 코드를 작성하는 스타일 가이드를 말한다.

문법만 맞으면 되는거 아닌가? 라는 생각을 할 수 있다. 하지만, 여려 사람들이랑 협업해서 하는 큰 프로젝트에서는 나만 알아보는 코드를 작성하기보다 모두가 알아들을 수 있는 코드를 작성하는 것이 필요하다. 이러한 경우에 하나의 통일된 스타일을 가지고 코딩을 하면 모두가 이해하기 쉬울 것이다. 그렇기 때문에, 스타일 가이드에 맞춰서 코딩을 하는 것이 중요하다.

스타일 가이드는 whitespace 몇개, tab 몇번 등 엄청 세부적으로 가이드를 제공한다. 하지만 그 중에서 제일 헷갈려하는 걸 짚어보려고 한다.

### Naming

- 함수, 변수, 속성의 이름은 lowercase_underscore 형식이어야 한다.

```python
def multiply_ten(a):
    return a*10

school_name = "H"
print(multiply_ten(10))
```


- Protected 인스턴스 속성은 _leading_underscore 형식이어야 한다.
- Private 인스턴스 속성은 __double_leading_underscore 형식이어야 한다.

```python
class Calculator:
    _protected = 10
    __pi = 3.14
...
```

- Class나 Exceptions는 CapitalizedWord 형식이어야 한다.

```python
try:
    ...
except ValueError:
    ...
```

- Module-level의 constant들은 ALL_CAPS 형식이어야 한다.

```python
# opencv
import cv2
cv2.CV_CAP_PROP_FPS 
```

### Expressions & Statements

- 비어있는 value 확인하기 위해서는 `if len(a)==0` 이런 식이 아니라 ⇒ `if not a` 라는 식으로 작성한다.
- 비어있지 않는 value 확인할 때도 비슷하다.
- `import ...` 는 항상 파일 맨 위에 위치한다.

## Item 3. bytes, str 차이점을 알자

Python3 에서 

- str는 내부적으로 `unicode` character를 갖고 있다.
- bytes는 `raw 8-bit` 값을 갖고 있다

unicode를 binary로 바꾸려면 `encode` method를 사용해야 하고, binary를 unicode로 바꾸려면 `decode` method를 사용해야 한다.

```python
# binary를 unicode로 변환하는 method
def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode(‘utf-8’)
    else:
        value = bytes_or_str
    return value # Instance of str


# unicode를 binary로 변환하는 method
def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode(‘utf-8’)
    else:
        value = bytes_or_str
    return value # Instance of bytes
```

 

Python3에서는 파일을 읽고 쓸 때 default로 utf-8 encoding을 사용한다. 그래서 binary파일을 바로 읽을 수 없다. 만약 binary 파일을 읽고 싶으면 `rb`, 쓰고 싶으면 `wb` 로 명시를 해줘야 한다.

```python
with open(‘/tmp/random.bin’, ‘w’) as f:
    f.write(os.urandom(10))

with open(‘/tmp/random.bin’, ‘wb’) as f:
    f.write(os.urandom(10))
```

## Item 7,8. List Comprehension

map, filter를 사용하는 것보다 list comprhension을 사용하는 것을 추천한다. List comprehension은 한 눈에 보기가 쉽기 때문이다.

```python
even_squares = [x**2 for x in a if x % 2 == 0]
print(even_squares)
```

하지만, 중첩으로 여러개의 list comprehension을 사용하는 것은 추천되지 않는다. List comprehension은 긴 코드를 줄여주는 효과를 내지만, 중첩이 길어지면 기존의 for loop을 중첩하는 것과 크게 다르지 않기 때문이다.

```python
# list comprehension
flat =[x for sublist1 in my_lists
    for sublist2 in sublist1
    for x in sublist2]

# for 중첩
flat = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        flat.extend(sublist2)
```


## Item 9. List Comprehension 클 때는 Generator 사용하기

또한, list comprehension이 매우 크다면 `Generator` 사용을 고려해야 한다. Input이 매우 크면 시간도 매우 오래 걸릴뿐더러 메모리도 많이 잡아먹기 때문이다. Generator는 전체 output을 한번에 연산을 하는 것이 아니라 iterator로 해당하는 expression에 도달하면 item을 하나씩 yield를 한다.

Generator는 list comprehension처럼 생긴 문법을 [] 가 아닌 ()에 두면 된다. 다만 generator를 바로 print하면 generator의 object이 반환될 것이다. 그래서 generator를 iterate하는 것이 중요하다. Iterate하면 iterate 할 때마다 연산을 하게 된다.

```python
it = (len(x) for x in open(‘/tmp/my_file.txt’))
print(it) 
# <generator object <genexpr> at 0x101b81480>

print(next(it))
print(next(it))
```


## Item 10. Enumerate

주로 Python으로 list를 iterate할 때 `for i in range(len(list_name))` 혹은 `for name in list_name` 형식을 많이 쓰는 경우가 있다. 

첫 번째 경우는 list의 크기만큼 iterate를 하고 index로 접근을 하고, 두 번째 경우는 각 iteration마다 item이 name 변수로 들어오게 된다. 

```python
fruit = ['banana', 'apple', 'orange', 'pineapple', 'melon']
for i in range(len(fruit)):
	print(fruit[i])

for f in fruit:
	print(f)
```

index로 접근하는 것보다 각 iteration마다 list의 item을 사용하는 것이 더 직관적이고 코드의 길이도 줄여준다. 하지만 프로그래밍을 하다보면 iteration을 할 때 index로 item에 접근할 필요가 있을 때가 있다. 예) 그 이전 item 혹은 그 이후 item에 접근할 때.

그 때 `enumerate` 를 사용하는 것이 가장 좋은 방법이고, 가능하면 range() 대신에 `enumerate` 을 사용하는 것이 좋다. `for i,f in enumerate(fruit)` 에서 앞에 `i` 는 index range에서처럼 index를 의미하고 `f` 는 fruit list의 iteration마다의 item을 의미한다.

```python
for i,f in enumerate(fruit):
	print(fruit[i])
	print(f)
	# 같은 것을 print함
```

## Item 11. List를 동시에 iterate하려면, zip

list가 여러개 있고 동시에 list를 iterate하고 싶은 경우가 있다. (default로 길이가 제일 짧은 list만큼만 iteration이 이뤄진다)

예) 유저 이름 list, 유저 나이 list가 따로 있을 때, 유저가 20세 이상일 때만 이름을 출력하고 싶을 때 

```python
name = ['Henry', 'Lisa', 'Dorosi', 'Gimmy']
age = [10, 22, 32, 17]

# 기존 방식
for i in range(len(name)):
	if age[i] > 20:
		print(name[i], age[i])


# zip
for n,a in zip(name,age):
	if a > 20:
		print(n,a)
```

이런 식으로 zip을 사용하게 되면 index으로 인해 복잡해지는 코드를 간결하게 줄 일 수 있다. zip은 여러 list를 하나로 묶어서 하나씩 iterate하는 역할을 한다.

## Item 13. try-except-else-finally

예외사항을 처리할 때 사용되는 명령어들이 있다: try, except, else, finally. Try는 주로 실행하려고 한는 구문에 에러가 있을 수 있을 때 사용을 한다. 

**except**는 어떤 error가 발생했는지 지정할 수 있다. 간단히 `Exception as e` 라고 할 수 있지만, exception의 종류도 많기 때문에 보통은 조금 상세하게 지정을 한다. 

**else**는 예상했던 exception이 발생하지 않았다면 다음 구문을 실행한다, 이 때 다른 exception이 발생할 수 있다. 

마지막으로 **finally**는 모든 구문이 실행되고 나서 맨 마지막에 항상 실행된다. Exception이 일어났을 때도 혹은 아무 exception이 일어나지 않았을 때도 finally는 실행이 된다.

```python
handle = open(‘/tmp/random_data.txt’):
try:
	data = handle.read()
	op = json.loads(data)
	value = (op[‘numerator’]/op[‘denominator’]) # 0이 분모로 오는 error가 발생할 수 있음 
except ZeroDivisionError as e:
	return e
else: # 0으로 나누는 error가 발생하지 않았다면 이 구문 실행
	op[‘result’] = value
	handle.write(result)  
finally:
	handle.close() # 다 실행이 됬다면 run함(error가 발생했던 안 발생했던간에)
```