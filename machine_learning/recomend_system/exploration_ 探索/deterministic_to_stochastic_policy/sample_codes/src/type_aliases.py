from typing import TypeAlias

import numpy as np

UserId: TypeAlias = str
ContentId: TypeAlias = str
MovieId: TypeAlias = str
NewsId: TypeAlias = str
Id: TypeAlias = UserId | MovieId | NewsId
Vector: TypeAlias = np.ndarray
PreferenceScore: TypeAlias = float
