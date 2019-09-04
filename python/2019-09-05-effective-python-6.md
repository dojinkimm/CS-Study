# Effective Python [파이썬 코딩의 기술] - Ch 6 - Built-in Module

해당 책은 다음의 링크에서 다운받을 수 있습니다 (영문) : [LINK](https://arisuchan.jp/λ/src/1498628824511-0.pdf)


# Item 42: functools.wraps로 함수 decorator 정의하기

Python은 감싸고 있는 함수 이전 혹은 그 이후에 특정한 코드를 실행시킬 수 있는 `decorator`라는 특별한 문법을 가지고 있다. 이 문법으로 입력 argument나 리턴 값을 수정할 수 있다, 디버깅할 때 유용하게 사용될 수 있다. 예를 들어, argument와 리턴 값을 프린트해서 진행상황을 보고 싶을 때 사용하기에 적절하다. 특히, 재귀함수가 어떻게 stack으로 쌓여가는지 볼 수 있게 된다.

`@` 를 추가해서 현재 함수에 `decorator`를 호출할 수 있게 된다. fibonacci 함수가 실행되기 전과 후에 wrapper를 실행시킨다.

```python
def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(‘%s(%r, %r) -> %r’ %(func.__name__, args, kwargs, result))
        return result
    return wrapper

@trace
def fibonacci(n):
    “““Return the n-th Fibonacci number”””
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))

fibonacci = trace(fibonacci)
fibonacci(3)

# fibonacci((1,), {}) -> 1
# fibonacci((0,), {}) -> 0
# fibonacci((1,), {}) -> 1
# fibonacci((2,), {}) -> 1
# fibonacci((3,), {}) -> 2
```


# Item 43: 재사용 가능한 try/finally 동작을 만들기 위해 contextlib 과 with 문 고려하기

`with` 문은 Python에서 코드가 특별한 context안에서 실행된다는 것을 의미한다. Item38에서 lock을 사용할 때 `with`문을 사용했었는데, 이 때 해당 문법 밑에 코드는 lock가 있을 때만 실행됨을 의미한다.

```python
lock = Lock()
with lock:
    print('Lock is held')
```

`with`에 해당하는 문법을 `try/finally` 로 똑같이 변환할 수 있다.

```python
lock.acquire()
try:
    print('Lock is held')
finally:
    lock.release()
```

하지만, `with`문을 사용한는 것이 더 간결하다. 

 

`with`문을 더 잘 사용하기 위해서는 `contextlib` built-in 모듈을 사용할 수 있다. 이 모듈은 `contextmanager`라는 decorator를 지니고 있어서 간단한 함수가 `with`문에 사용될 수 있게 한다. 

debug logging을 하는 코드가 있다고 가정해보자. 프로그램의 기본 log level은 WARNING이다, 그래서 함수를 실행했을 때 error 메세지만 프린트 된다.

```python
def my_function():
    logging.debug('Some debug data')
    logging.error('Error log here')
    logging.debug('More debug data')

my_function()
# Error log here
```

context manager를 사용해서 일시적으로 log level을 변경할 수 있다. 이 helper함수는 `with` 블록에서 사용될 때와 아닐 때 다른 logging severity level을 다르게 한다.

```python
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)
```

`yield`는 `with`블록이 실행될 포인트이다. 밑에 코드를 실행시켰을 때 `with` 블록 안에서 함수를 호출했을 때는 모든 debug정보들이 프린트 됌을 알 수 있다. 이처럼 `with`안에 있을 때는 특정한 context로 실행이 되도록것이다.

```python
with debug_logging(logging.DEBUG):
    print(‘Inside:’)
    my_function()
print(‘After:’)
my_function()

# Inside:
# Some debug data
# Error log here
# More debug data
# After:
# Error log here
```

### `with` Target  사용하기

`with`문에 전달된 context manager는 object를 리턴할 때도 있다. 이 object를 `as`로 특정한 로컬 변수에 지정할 수 있다.

`open`의 리턴 object가 `with`문 내에서만 사용할 수 있는 로컬변수 handle에 저장이 되고 사용할 수 있다.

```python
with open(‘/tmp/my_output.txt’, ‘w’) as handle:
    handle.write(‘This is some data!’)
```


# Item 44: copyreg로 pickle을 신뢰할 수 있게 만들기

### Note

Python의 `pickle`모듈은 사실 디자인적으로 안전하지 않다. Serialized data는 다시 Python object로 어떻게 만들지에 대한 정보를 가지고 있다. 그래서 잘못된 정보를 포함시키게 만들면 deserialize해서 Python object를 만들 때 잘못된 Python object가 만들어질 수 있다. 반면에, `json`모듈의 디자인은 안전하다. 

`pickle`은 Python object를 bytes stream으로 serialize(직렬화)하고 다시 butes를 object로 deserialize하게 해주는 built-in 모듈이다. 

게임에서 플레이어 진행상황을 알려주는 코드를 작성해보자. 게임을 진행하면서 상태가 바뀌고 게임을 종료할 때 현재 상태를 파일에 `pickle`모듈로 저장한다. `pickle`모듈의 `dupm`로 GameState object를 파일에 바로 저장할 수 있게 된다. 그리고 `load`로 저장된 파일을 불러올 수 있다.

```python
class GameState(object):
    def __init__(self):
        self.level = 0
        self.lives = 4

state = GameState()
state.level += 1 
state.lives -= 1 

# 파일 저장
state_path = '/tmp/game_state.bin'
with open(state_path, ‘wb’) as f:
    pickle.dump(state, f) 

# 파일 불러오기
with open(state_path, ‘rb’) as f:
    state_after = pickle.load(f)
print(state_after.__dict__)

# {‘lives’: 3, ‘level’: 1}
```

이 게임에서 플레이어는 고득점을 목표로 한다고 가정해보자. 그러기 위해서는 플레이어들의 점수를 알아야 하기에 GameState class에 새로운 field를 추가해준다. 새로운 class에다 `dump`를 하고 `load`를 다시하면 이전에 있던 정보가 없어진 것을 볼 수 있다.

그래서 이전 object의 내용을 path로 불러오면 제대로 불러와진 것을 볼 수 있다, 하지만, 새로 추가된 points라는 attribute는 사라졌다. 

```python
class GameState(object):
    def __init__(self):
        self.level = 0
        self.lives = 4
        self.points = 0 # 추가된 부분

state = GameState()
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)

# {‘lives’: 4, ‘level’: 0, ‘points’: 0}

with open(state_path, ‘rb’) as f:
    state_after = pickle.load(f)
print(state_after.__dict__)

# {‘lives’: 3, ‘level’: 1}
```

이러한 문제를 해결하기 위해서는 `copyreg` built-in 모듈을 사용해야 한다.

처음에 default value들을 constructor에 추가해준다. `unpickle_game_state`함수는 serialized data와 parameter를 `pickle_game_state`에서 받고 이에 해당하는 GameState object를 리턴한다. constructor를 감싸는 wrapper정도라고 생각하면 된다.

```python
class GameState(object):
    def __init__(self, level=0, lives=4, points=0):
        self.level = level
        self.lives = lives
        self.points = points

    def pickle_game_state(game_state):
        kwargs = game_state.__dict__
        return unpickle_game_state, (kwargs,)

    def unpickle_game_state(kwargs):
        return GameState(**kwargs)
```

그 다음에 `copyreg`모듈을 register한다. 그러고 이전에 수행했던 작업을 해보면 원하는 만큼 points의 값이 올라간 걸 알 수 있다. 이제 GameState에 새로운 field를 추가해본다.

```python
copyreg.pickle(GameState, pickle_game_state)

state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)

# {‘lives’: 4, ‘level’: 0, ‘points’: 1000}
```

magic이라는 값을 추가해본다. 추가하고 나서 `pickle`로 load를 하면 magic attribute가 프린트됨을 볼 수 있다. 옛 GameState를 deserialize해도 바뀐 attribute가 있음을 알 수 있다. 이렇게 되는 이유는 `unpickle_game_state`가 GameState constructor를 바로 호출하기 때문이다. parameter가 비어있으면 defalut value를 바로 가져온다, 그래서 이전 game state 파일에 magic이 없었음에도 deserialize했을 때 magic의 default 값을 가져온 것이다. 

```python
class GameState(object):
    def __init__(self, level=0, lives=4, points=0, magic=5):
            # …


state_after = pickle.loads(serialized)
print(state_after.__dict__)

# {‘level’: 0, ‘points’: 1000, ‘magic’: 5, ‘lives’: 4}
```

### Versoning Classes


위 예시와 반대로 field를 제거해야될 때도 있다. GameState에서 lives field가 제거되었다고 가정해보고 어떤 결과가 나오는지 살펴보자

```python
class GameState(object):
    def __init__(self, level=0, points=0, magic=5):
            # …

pickle.loads(serialized)

# TypeError: __init__() got an unexpected keyword argument ‘lives’
```

field를 제거하면 TypeError가 발생한다. 이 에러를 방지하기 위해서는 `copyreg`에 버전 parameter를 추가하는 것이다. 이전 버전에는 version argument가 없었기 때문에 GameState가 constructor로 전달된다. 그러고 나면 이전 object를 deserialize하는 작업은 작동이 되게 된다.

```python
...
    def pickle_game_state(game_state):
        kwargs = game_state.__dict__
        kwargs['version'] = 2
        return unpickle_game_state, (kwargs,)

    def unpickle_game_state(kwargs):
        version = kwargs.pop('version', 1)
        if version == 1:
            kwargs.pop('lives')
        return GameState(**kwargs)



copyreg.pickle(GameState, pickle_game_state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)

# {‘magic’: 5, ‘level’: 0, ‘points’: 1000}
```


# Item 45: 지역시간은 time 대신에 datetime으로 표현하기

Python은 time을 2가지 방법으로 나타낸다. 오래된 방법은 `time` built-in 모듈을 사용하는 것인데, 에러가 매우 많다... `datetime`은 새로운 방법으로 커뮤니티에서 만든 `pytz`패키지와 같이 사용하면 매우 유용하다.

`datetime`예시를 살펴보기 전에 왜 `time`모듈은 사용하지 않는 것이 좋은지 살펴보자.

### `time` Module

`localtime`함수는 UNIX timestamp를 컴퓨터 타임 존의 local 시간으로 변환을 해준다.

```python
from time import localtime, strftime

now = 1407694710
local_tuple = localtime(now)
time_format = ‘%Y-%m-%d %H:%M:%S’
time_str = strftime(time_format, local_tuple)
print(time_str)

# 2014-08-10 11:18:30
```

하지만, 다른 타임 존의 local시간으로 변경하려면 어떻게 해야 할까? 예를 들어, 샌프란시스코에서 뉴욕의 시간을 알고 싶을 때, `time, localtime, strptime`함수들로 시간을 알아내기 힘들 것이다.

현재 컴퓨터가 Pacific Daylight Time 이라는 타임 존에 있다고 생각해보자. 이때 시간에 접근하는 것은 올바른 결과를 리턴해줄 것이다. 하지만 현 컴퓨터에서 다른 타임존 예를 들어 Eastern Daylight Time에 접근하려고 하면 에러가 생기게 된다.

```python
parse_format = '%Y-%m-%d %H:%M:%S %Z'
depart_sfo = '2014-05-01 15:45:16 PDT'
time_tuple = strptime(depart_sfo, parse_format)
time_str = strftime(time_format, time_tuple)
print(time_str)

# 2014-05-01 15:45:16

arrival_nyc = '2014-05-01 23:33:24 EDT'
time_tuple = strptime(arrival_nyc, time_format)

# ValueError: unconverted data remains: EDT
```

이렇게 에러가 발생하는 이유는 `time` 모듈이 플랫폼에 종속적이기 때문이다. 이러한 성질 때문에 `time` 모듈 보다 `datetime` 모듈을 사용한는 것이 더 낫다.

### `datetime` Module

Python 커뮤니티에서 모든 타임 존에 대한 database를 `pytz`라는 모듈에 진니고 있다. 이 `pytz` 모듈을 사용하면 다른 타임존의 시간도 쉽게 알아낼 수 있다.

```python
from datetime import datetime, timezone

arrival_nyc = '2014-05-01 23:33:24'
nyc_dt_naive = datetime.strptime(arrival_nyc, time_format)
eastern = pytz.timezone('US/Eastern')
nyc_dt = eastern.localize(nyc_dt_naive)
utc_dt = pytz.utc.normalize(nyc_dt.astimezone(pytz.utc))
print(utc_dt)

# 2014-05-02 03:33:24+00:00

pacific = pytz.timezone('US/Pacific')
sf_dt = pacific.normalize(utc_dt.astimezone(pacific))
print(sf_dt)

# 2014-05-01 20:33:24-07:00
```



# Item 46: Built-in 알고리즘과 데이터 구조 사용하기

Python에서 작은 데이터에 대해 직접 구현한 알고리즘을 적용하면 속도가 저하되는 일이 때때로 있다. Python 자체가 느리기 보다는 보통 유저가 문제에 최적화된 알고리즘을 적용하지 않았기 때문에 발생하는 것이다.

이러한 문제점을 해결하기 위해 Python은 알고리즘과 데이터구조를 사용할 수 있는 표준 라이브러리들을 제공한다.  



### Double-ended Queue

`collections` 모듈의 `deque` class는 doube-ended queue이다. 그렇기 때문에 item을 앞이나 뒤에서 삽입 혹은 제거하는 시간은 상수 시간만큼 걸린다 O(1). 


```python
que = deque()
que.append(1)
x = que.popleft()
```


사실 `list`도 queue 형식의 데이터 구조이다. 하지만 `deque`와는 달리 뒤에 삽입 혹은 제거할 때만 상수 시간만큼 걸린다. 맨 앞에 삽입 혹은 제거할 때는 linear 시간만큼 걸린다.



### Ordered Dictionary

표준 dictionary는 정렬되어있지 않다. 두개의 dictionary가 있고 같은 key와 value를 지녔더라도 iteration할 때 다른 순서대로 진행될 수 있다. 하지만 이 방법 덕분에 빠른 hash table을 구현할 수 있었다.

`OrderedDict`는 `collections` 모듈의 class이고 key가 삽입되는 대로 순서를 저장하는 특별한 dictionary 타입이다. `OrderedDict`에서 key를 예측 가능하게 iterate(순회)한다.

```python
a = OrderedDict()
a[‘foo’] = 1
a[‘bar’] = 2

b = OrderedDict()
b[‘foo’] = 'red'
b[‘bar’] = 'blue'

for value1, value2 in zip(a.values(), b.values()):
    print(value1, value2)

# 1 red
# 2 blue
```


### Default Dictionary

Dictionary는 bookkeeping이나 지표들을 추적할 때 유용하다. 하나 문제점은 key가 dictionary에 이미 있는지 확인할 수 없다는 것이다. 그래서 밑의 코드와 같이 불필요한 작업을 하게 되는 것이다.

```python
stats = {}
key = 'my_counter'
if key not in stats:
    stats[key] = 0
stats[key] += 1

```


`collections` 모듈의 `defaultdict` class는 자동적으로 없는 key에 default 값을 저장해서 위 문제를 해결한다. parameter로 default 값이 무엇일지 정해줄 수 있다. `int`는 built-in 함수로 0을 리턴한다.

```python
stats = defaultdict(int)
stats['counter'] += 1
```



### Heap Queue

Heap은 우선순위 queue를 유지하는데 유용한 데이터 구조이다. `heapq`라는 모듈은 표준 `list`타입에 `heappush`, `heappop`, `nsmallest`와 같은 기능들을 사용할 수 있게 해준다.

Item 들은 아무 순서로 heap에 추가가 가능하다. 제거할 때는 항상 높은 우선순위(낮은 숫자)부터 제거된다. 

```python
a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 4)

print(heappop(a), heappop(a), heappop(a), heappop(a))

# 3 4 5 7
```

0 index는 항상 가장 작은 item을 리턴한다. `heapq`의 자겁들은 항상 list길이에 비례해 log 시간만큼 걸린다.

```python
a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 4)
assert a[0] == nsmallest(1, a)[0] == 3
```



### Bisection

`index` method를 사용해서 `list`의 item을 찾을 때 linear 시간만큼 걸린다. `bisect` 모듈의 함수인 `bisect_left`는 정렬된 item에서 더 효율적인 binary search(이진 탐색)을 제공한다. 해당 값이 삽입된 index를 리턴한다.

binary search의 시간 복잡도는 O(logn)이다. 반면 `list`의 시간복잡도는 O(n)이기 때문에, index를 찾을 때는 `bisect`를 사용하면 더 빠르게 찾을 수 있다.

```python

x = list(range(10**6))
i = x.index(991234)

i = bisect_left(x, 991234)
```



### Iterator Tools

`itertools`는 iterator를 다루는 모듈이다. `itertools`는 크게 3개의 메인 카테고리로 나뉘어져있다:

1. iterator들을 link
    - `chain` - 여러 iterators를 하나의 순차적인 iterator로 합침
    - `cycle` - iterator의 item들을 무한대로 반복한다
    - `tee` - 하나의 iterator를 여러개의 parallel한 iterator들로 나눈다
    - `zip_longest` - `zip` 함수인데 다른 길이의 iterator와도 잘 작동한다
2. iterator에서 item 필터링
    - `islice` - 복사하지 않고 여러 index들로 iterator를 slice한다
    - `takewhile` - 함수가 True일 때 item을 계속 리턴한다
    - `dropwhile` - 함수가 처음으로 False일 때 item을 리턴한다
    - `filterfalse` - 함수가 False일 때 모든 item들을 리턴한다. `filter` 함수의 반대 역할을 한다
3. item의 combination
    - `product` - item들의 Cartesian product를 리턴한다.
    - `permutations` - 순열을 리턴한다
    - `combination` - 조합을 리턴한다

이외에도 많은 함수들이 `itertools`에 있다.



# Item 47: 정밀도가 중요할 때는 decimal 사용하기

Python에서 소수점을 다룰 때 조심해야 한다. 밑에 처럼 반올림될때 소숫점 2번째 자리까지 나타내려고 할 때 그냥 0으로 만들어버리는 경우가 있다. 이런 결과는 유저가 원하지 않은 결과일 가능성이 높다.  

```python
rate = 0.05
seconds = 5
cost = rate * seconds / 60
print(cost)
# 0.004166666666666667

print(round(cost, 2))
# 0.0
```


이러한 문제점을 해결하기 위해서는 `decimal` built-in 모듈의 `Decimal` class를 사용해야 한다. `Decimal` class는 default로 28개의 고정된 decimal points를 제공한다. 요구한다면 더 많은 숫자의 decimal points를 제공할 수도 있다. 

`quantize` method를 사용하면 round될 때 정확한 approximation을 얻을 수 있다.

```python
rate = Decimal(‘0.05’)
seconds = Decimal(‘5’)
cost = rate * seconds / Decimal(‘60’)
print(cost)

# 0.004166666666666666666666666667

rounded = cost.quantize(Decimal(‘0.01’), rounding=ROUND_UP)
print(rounded)

# 0.01
```