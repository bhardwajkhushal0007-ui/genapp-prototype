import random
from genetics import MARKERS
def random_profile():
    return {m:(str(random.randint(8,24)),str(random.randint(8,24))) for m in MARKERS}
if __name__ == "__main__":
    for i in range(5): print(f"PROFILE-{i+1}", random_profile())
