# CUMCM2018

A private repository working on Problem B of CUMCM 2018

## To Do

- [ ] Encode job schedule on chromosome

## Notes

Notes are copied from the problem description and its appendix.

### RGV

- RGV 机械手臂前端有 2 个手爪，通过旋转可以先后各抓取 1 个物料，完成上下料作业。
- RGV 同一时间只能执行移动、停止等待、上下料和清洗作业中的一项
- 清洗作业时间: 首先用另一只机械手抓取出清洗槽中的成料、转动手爪、放入熟料到清洗槽中，然后转动机械臂，将成料放到下料传送带上送出系统。这个作业过程所需要的时间称为 RGV 清洗作业时间。

### CNC

如果物料的加工过程需要两道工序，则需要有不同的 CNC 安装不同的刀具分别加工完成，在加工过程中不能更换刀具。第一和第二道工序需要在不同的 CNC 上依次加工完成，完成时间也不同，每台 CNC 只能完成其中的一道工序。
