# <center> 训练结果分析

### 1. confusion_matrix（混淆矩阵）

**改进前模型：**
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp3\confusion_matrix.png]]

**改进后模型：**
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp7\confusion_matrix.png]]

该混淆矩阵行表示预测类别，列表示真实类别，对角线元素表示正确分类，非对角线元素显示错误分类。
**对角线准确率：** *以下数据为改进后vs改进前，*改进后Attentive：0.93 vs 0.97、Eye-Close：0.86 vs 0.89、Eye-Open：0.92 vs 0.94、Inattentive：0.96 vs 0.97和Yawning：0.99 vs 1.00，略有下降，Normal保持0.97不变；整体主类识别率微降0.02-0.04，表明分类边界稍模糊。

**背景误分类率：**Eye-Close和Eye-Open的背景误分类率降低（0.18 vs 0.37）、（0.33 vs 0.41），其他类背景干扰减少，改进后背景噪声处理更稳健，减少了约20%的假阴性。

**类间混淆：**Eye-Close与Eye-Open间混淆略增，但<font color="#ff0000">Inattentive与Normal间混淆显著降低</font>，整体类间错误率下降，分类鲁棒性提升。

**比较：**改进后背景分辨能力更强，减少了20%假阴性，分类边界更清晰，但是Eye-Close的检测能力略弱。

### 2. F1_curve(F1曲线)

**改进前模型：**
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp3\F1_curve.png]]

**改进后模型：**
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp7\F1_curve.png]]

改进后的峰值F1为0.94 @0.374，曲线在低置信区域（低于0.4）更陡峭，高置信区（大于0.6）的F1下降0.02，Yawming 和 Normal提升0.01，表明在平衡recall时更高效

**比较：**改进后的F1平衡性增强，适用于低阈值场景，但是峰值微降，适合实时应用中的快速决策。

### 3. P_curve（精确度与置信度）

**改进前模型：**
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp3\P_curve.png]]

**改进后模型：**
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp7\P_curve.png]]

改进后所有类在置信度0.994时达到1.00percision（改进前模型为0.993），曲线更为平滑，Eye-Close和Inattentive在高置信区（>0.8）提升约0.02，但整体峰值持平，表明峰值优化更精确

**比较：**置信上限微升，阈值优化更精确，Eye-Close等类得到一定优化，但无大幅提升。

### 4. R_curve（召回率与置信度）

**改进前模型：**
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp3\R_curve.png]]

**改进后模型：**
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp7\R_curve.png]]

改进后的所有类在0.000置信度下recall达0.98，与改进前持平，但高置信区（>0.6）Eye-Close recall提升0.03，整体曲线更平缓，减少了高阈值下的漏检。

**比较：**改进后召回稳定性更好，减少了疲劳检测中的遗漏风险。

### 5. PR_curve（精确度与召回率）

改进前模型：
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp3\PR_curve.png]]

改进后模型：
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp7\PR_curve.png]]

整体mAP@0.5微降（0.960->0.952），但Inattentive提升（0.968->0.973），Eye-Close下降（0.891->0.851）；mAP@0.5:0.95为0.667，召回敏感类略降，平衡性稍弱。

**比较：**平衡性略弱，但Inattentive提升，表明针对疲劳驾驶的检测优化有效。

### 6.results.png & result.csv（训练指标图与日志）

改进前模型：
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp3\results.png]]
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp3\results.csv]]

改进后模型：
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp7\results.png]]
![[E:\大创相关\OrangePi_Project\workspace\yolov5-master_test1\yolov5-master_test\runs\train\exp7\results.csv]]

**提升点：**

- 平均训练obj_loss（0.0134 → 0.0125）和cls_loss（0.0062 → 0.0055）降低，对象检测和分类更准确。
- 验证obj_loss和cls_loss略有改善，泛化能力小幅提升。
- 初始精度更高（0.794 vs 0.751），早期稳定增强。

### 总结

改进后的模型在背景抑制、召回稳定性和训练的鲁棒性上有明显提升，体现在R_curve + 3%、混淆矩阵错误 -5%,该模型更适合驾驶监控的噪声环境，整体改进幅度中等。
