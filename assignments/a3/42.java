/*
Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it is able to trap after raining.

For example, 
Given [0,1,0,2,1,0,1,3,2,1,2,1], return 6.
*/
class Solution {
    public int trap(int[] height) {
        int[] left = new int[height.length];
        int[] right = new int[height.length];
        int max = 0;
        for(int i=0;i<left.length;i++){
            if(max<=height[i])
                max = height[i];
            else
                left[i] = max;
        }
        max = 0;
        for(int i=left.length-1;i>=0;i--){
            if(max<=height[i])
                max = height[i];
            else
                right[i] = max;
        }        
        int total = 0;
        for(int i=left.length-1;i>=0;i--){
            if(left[i]==0||right[i]==0)
                continue;
            else
                total+=Math.min(left[i],right[i])-height[i];
        }
        return total;
            
    }
}