"""
우주 거래소의 시계 (space_exchange_sim.py 별칭 래퍼)
파일명에 하이픈(-)을 사용하는 사용자를 위해 physics_sim/space_exchange_sim.py를 실행합니다.
"""
import os
import runpy

target_file = os.path.join(os.path.dirname(__file__), "space_exchange_sim.py")
runpy.run_path(target_file, run_name="__main__")
