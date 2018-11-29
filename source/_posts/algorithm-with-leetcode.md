---
title: leetcode 算法刷题记录
categories:
  - leetcode
tags:
  - Python
  - Go
  - leetcode 算法
toc: true
date: 2018-11-30 00:30:13
---

leetcode 算法刷题记录和总结, 主要使用Python和Go来作答.

## 算法
#### 从排序数组中删除重复项
给定一个有序数组，你需要原地删除其中的重复内容，使每个元素只出现一次,并返回新的长度。不要另外定义一个数组，您必须通过用 O(1) 额外内存原地修改输入的数组来做到这一点。
##### 示例
给定数组: nums = [1,1,2], 你的函数应该返回新长度 2, 并且原数组nums的前两个元素必须是1和2
不需要理会新的数组长度后面的元素
##### 思路
数组是有序的, 则相同的值必定是紧挨着的, 通过定义两个变量,  一个变量a用于记录数组最后一个不重复值的下标, 使用一个变量b循环数组, 若nums[a] != nums[b] 时, 就将a值增1, 并执行nums[a] = nums[b]. 循环结束后, a+1 的值即为数组中新数组不相等的长度. 考虑到空数组的情况, 可将b初始化为-1, 在循环结束后 b > a 的情况下, 才将a增1.
##### 代码
Python:
```python
class Solution:
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        diff_length = 0
        index = -1
        for index, item in enumerate(nums): 
            if nums[diff_length] != item:
                diff_length += 1
                nums[diff_length] = item

        if index >= diff_length:
            return diff_length + 1
        else:
            return diff_length
```
Go:
```go
func removeDuplicates(nums []int) int {
    ix := -1
	var val int
	diffLength := 0

	for ix, val = range nums {
		if nums[diffLength] != val {
			diffLength++
			nums[diffLength] = val
		}
	}

	if ix >= diffLength {
		diffLength++
	}
    
    return diffLength
}
```

#### 旋转数组
将包含 n 个元素的数组向右旋转 k 步。要求空间复杂度为 O(1)。
##### 示例
例如，如果  n = 7 ,  k = 3，给定数组  [1,2,3,4,5,6,7]  ，向右旋转后的结果为 [5,6,7,1,2,3,4]。
##### 思路
1. 旋转数组操作类似于一个循环队列操作, k 到队尾出队再从对首入队
2. 利用切片操作将数组切为 [:len(nums)-k] 和 nums[len(nums)-k:] 再重新组合
3. 将数组 [:len(nums)-k] 和 [len(nums)-k:] 分别逆序, 再将整个数组逆序
##### 代码
Python:
思路1
```python
class Solution:
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        step = k % len(nums)
        for index in range(step):
            nums.insert(0, nums.pop())
```
思路2:
```python
class Solution:
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        k = k % len(nums)
        nums[:k], nums[k:] = nums[len(nums)-k:], nums[:len(nums)-k]
```
Go:
```go
func rotate(nums []int, k int)  {
    n := len(nums)
    k %= n
    k = n - k
    reverse(nums[:k])
    reverse(nums[k:])
    reverse(nums)
}

func reverse(nums []int) {
    for i, j := 0, len(nums) - 1; i < j; i, j = i + 1, j - 1 {
        nums[i], nums[j] = nums[j], nums[i]
    }
}
```

#### 两个数组的交集 II
给定两个数组，写一个方法来计算它们的交集。
- 输出结果中每个元素出现的次数，应与元素在两个数组中出现的次数一致。
- 我们可以不考虑输出结果的顺序。

##### 示例
例如, 给定 nums1 = [1, 2, 2, 1], nums2 = [2, 2], 返回 [2, 2].

##### 思路
便利其中一个列表(可能的话, 优先选择较短的数组), 检查此列表中的元素是否在另一列表中存在, 存在的话即为一交集值加入返回结果的列表中, 并从了另一列表中删除

##### 代码
Python:
思路1
```python
class Solution:
    def intersect(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        set_list = []
        for item in nums1:
            if item in nums2:
                set_list.append(item)
                nums2.remove(item)

        return set_list
```
思路2, 利用`collections`模块
```
import collections

class Solution:
    def intersect(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        import collections
        return list((collections.Counter(nums1)&collections.Counter(nums2)).elements())
```

Go:
```go
func intersect(nums1 []int, nums2 []int) []int {
    setList := []int{}

	tmpMap := make(map[int]int)
	for _, item := range nums1 {
		_, ok := tmpMap[item]
		if ok {
			tmpMap[item]++
		} else {
			tmpMap[item] = 1
		}
	}
	for _, item := range nums2 {
		_, ok := tmpMap[item]
		if ok && tmpMap[item] > 0 {
			setList = append(setList, item)
			tmpMap[item]--
		}
	}
    
    return setList
}
```

#### 两数之和
给定一个整数数组和一个目标值，找出数组中和为目标值的两个数。你可以假设每个输入只对应一种答案，且同样的元素不能被重复利用。

##### 示例
给定 nums = [2, 7, 11, 15], target = 9 因为 nums[0] + nums[1] = 2 + 7 = 9 所以返回 [0, 1]

##### 思路
1. 循环遍历, 依次相加验证
2. 利用 map 来验证差是否在数组中

##### 代码
Python:
思路1
```python
class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for index1 in range(len(nums)-1):
            num1 = nums[index1]
            for index2, num2 in enumerate(nums[index1+1:]):
                if num1 + num2 == target:
                    return [index1, index2+index1+1]

        return []
```

Go:
思路2
```go
func twoSum(nums []int, target int) []int {
	numMap := make(map[int]int)
    
	for index1, item := range nums {
		num := target - item
		index2, ok := numMap[num]
		if ok {
			return []int{index2, index1}
		}
		numMap[item] = index1
	}

	return []int{}
}
```
