# example of using test cases to debug
## testing the find_rotated_point function, calculated by hand
### Test Case 1  
**Input:** (x1, y1, angle) = (0, 1, 90)  
**Computation Steps:**  
- \( x_2 = 0 * cos(90°) - 1 * sin(90°) = 0 - 1 = -1.0 \)  
- \( y_2 = 0 * sin(90°) + 1 * cos(90°) = 0 + 0 = 0.0 \)  
**Expected Output:** [-1.0, 0.0]  
**Actual Output:** [-1.0, 0.0]  
**Result:** ✅ Pass  

---

### Test Case 2  
**Input:** (x1, y1, angle) = (0, 1, 180)  
**Computation Steps:**  
- \( x_2 = 0 * cos(180°) - 1 * sin(180°) = 0 - 0 = 0.0 \)  
- \( y_2 = 0 * sin(180°) + 1 * cos(180°) = 0 - 1 = -1.0 \)  
**Expected Output:** [0.0, -1.0]  
**Actual Output:** [0.0, -1.0]  
**Result:** ✅ Pass  

---

### Test Case 3  
**Input:** (x1, y1, angle) = (0, 1, 270)  
**Computation Steps:**  
- \( x_2 = 0 * cos(270°) - 1 * sin(270°) = 0 + 1 = 1.0 \)  
- \( y_2 = 0 * sin(270°) + 1 * cos(270°) = 0 + 0 = 0.0 \)  
**Expected Output:** [1.0, 0.0]  
**Actual Output:** [1.0, 0.0]  
**Result:** ✅ Pass  
