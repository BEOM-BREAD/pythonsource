# 영어타자 프로그램
import random, time

# word.txt 읽어서
words = []
with open("./ch1/data/word.txt", "r", encoding="utf-8") as f:
    for word in f:
        words.append(word.strip())
# 임의로 하나 추춝 random.choice()

# Q1) then
# input()
# input() 결과에 따라서 정답 !! or 오타!!

start = time.time()

score = 0

# 문제 5문제 출제
for i in range(5):
    # 섞는다 random.shuffle()
    random.shuffle(words)
    q = random.choice(words)
    print(f"문제{i + 1}): {q}")

    answer = input("입력 :")

    if answer.strip() == q:
        print("정답!!")
        score += 1
    else:
        print("오타!!")

end = time.time()
# 게임시간 출력
# 정답 개수
# 출력문 => 게임시간 : 10초, 정답개수 : 3개
print(f"게임시간 : {end - start:.1f}초")
print(f"정답개수 : {score}개")

# 3개 이상 정답인 경우 합격 or 불합격
if score >= 3:
    print("합격")
else:
    print("불합격")