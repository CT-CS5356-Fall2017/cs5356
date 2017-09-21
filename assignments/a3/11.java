/*
Given n non-negative integers a1, a2, ..., an, where each represents a point at coordinate (i, ai). n vertical lines are drawn such that the two endpoints of line i is at (i, ai) and (i, 0). Find two lines, which together with x-axis forms a container, such that the container contains the most water.

Note: You may not slant the container and n is at least 2.
*/

class Solution {
    public int maxArea(int[] height) {
        int l=0;
        int r =height.length-1;
        int max = 0;
        while(l<r){
            max = Math.max(max,Math.min(height[r],height[l])*(r-l));
            if(height[l]<height[r])   //move small endian to scan all max pair
                l++;
            else
                r--;
        }
        return max;
    }
}