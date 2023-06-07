import random
import importlib


class Action:
    def move(self, player, direction):
        move = importlib.import_module("main").move
        if direction == "up":
            move((player.x, player.y - 1))
        if direction == "down":
            move((player.x, player.y + 1))
        if direction == "left":
            move((player.x + 1, player.y))
        if direction == "right":
            move((player.x - 1, player.y))

    def arrow(self, player, direction):
        shoot_arrow = importlib.import_module("main").shoot_arrow
        if direction == "up":
            shoot_arrow((player.x, player.y + 1))
        if direction == "down":
            shoot_arrow((player.x, player.y - 1))
        if direction == "left":
            shoot_arrow((player.x - 1, player.y))
        if direction == "right":
            shoot_arrow((player.x + 1, player.y))


# 1. 인풋 받기 - 초기화, 현재위치, 화살개수
def current_status(playerPos, rooms, arrow):
    # rooms에서 view가 true인것만 볼수있다. room에서 받아올값. status, sensor
    # 확률연산
    # 필요없는 액션 제거 - 벽, 화살없음.
    print("onoe")


# 3. 행동판단
# 4. 리턴값 도출


def choose_action(actions, probabilities=None):
    """
    주어진 actions와 확률에 따라 액션을 선택하는 함수입니다.

    매개변수:
      actions (list): 가능한 액션들의 목록
      probabilities (list, optional): 각 액션이 선택될 확률. 기본값은 균일한 확률 분포입니다.

    반환값:
      선택된 액션
    """

    if probabilities is None:
        # 확률이 주어지지 않은 경우, 각 액션에 대해 동일한 확률로 선택
        probabilities = [1 / len(actions)] * len(actions)
    else:
        # probabilities가 주어진 경우, 음수나 합계가 1이 아닌 경우 오류 처리
        if any(p < 0 for p in probabilities) or round(sum(probabilities), 10) != 1:
            raise ValueError("확률은 각각 양수이며 합계는 1이여야 합니다.")

    # 주어진 확률에 따라 액션 선택
    return random.choices(actions, weights=probabilities)


# 예제 사용
actions = ["A", "B", "C"]
probabilities = [0.2, 0.3, 0.5]
selected_action = choose_action(actions, probabilities)
print(f"선택된 액션: {selected_action}")
