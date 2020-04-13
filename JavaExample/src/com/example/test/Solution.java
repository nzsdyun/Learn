/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.example.test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

class Solution {

    public static void main(String[] args) {
//        List<String> generateParentesis = generateParenthesis2(2);
//        System.out.println("generateParentesis:" + generateParentesis);
//        boolean isomorphic = isIsomorphic("ab", "aa");
//        System.out.println("isomorphic:" + isomorphic);
//          String licensePlate = "1s3 PSt";
//          String[] words = new String[] {
//              "step","steps","stripe","stepple"
//          };
//          String rw = shortestCompletingWord(licensePlate, words);
//          System.out.println("rw = " + rw);
//            List<String> rt = subdomainVisits(new String[] {"9001 discuss.leetcode.com"});
//           int[] result = plusOne(new int[] {6,1,4,5,3,9,0,1,9,5,1,8,6,7,0,5,5,4,3});
//          System.out.println("result = " + Arrays.toString(result));
//        int s = searchInsert(new int[] {1,3,5,6}, 5);
//          System.out.println("s = " + s);
//            printPascalTriangle(10);
//            System.out.println(getRow(6).toString());;
//            testListBubbleSort();
            testQuickSort();
    }
    
    private static void testQuickSort() {
        int[] a = new int[] {2, 6, 4, 5, 8, 12, -12, 3};
        quickSort(a, 0, a.length - 1);
        printArr(a);
    }
    
    private static void printArr(int[] a) {
        for (int i = 0; i < a.length; i++) {
            System.out.print(a[i] + ",");
        }
        System.out.println("");
    }
    
    public static void quickSort(int[] arr, int start, int end) {
        // 分治思想，选取一个基准值，每次将数组分成两区，左边全部小于基准值，右边全部大于基准值。
        if (start >= end) {
            return;
        }
        int mid = partitionFillPit(arr, start, end);
        quickSort(arr, start, mid - 1);
        quickSort(arr, mid + 1, end);
    }
    
    public static int partitionFillPit(int[] a, int start, int end) {
        // 将第一个元素作为基准值（第一个坑位）
        int pivot = a[start];
        while (start < end) {
            while (a[end] >= pivot && start < end) end--;
            // 将小于基准值的元素填入先前的坑位，并将此元素的位置作为新的坑位
            a[start] = a[end];
            while (a[start] <= pivot && start < end) start++;
            // 将大于基准值的元素填入先前的坑位，并将此元素的位置作为新的坑位
            a[end] = a[start];
        }
        //归位基准值
        a[start] = pivot;
        return start;
    }
    
    public static int partition(int[] a, int start, int end) {
        // 将第一个元素作为基准值
        int pivot = a[start];
        int left = start;
        int right = end;
        while (left < right) {
            // 从右边查找不小于基准值的元素
            while (a[right] >= pivot && left < right) right--;
            // 从左边查找不大于基准值的元素
            while (a[left] <= pivot && left < right) left++;
            if (left < right) {
                // 交换左右两边的值
                int temp = a[left];
                a[left] = a[right];
                a[right] = temp;
            }
        }
        // 归位基准值
        a[start] = a[left];
        a[left] = pivot;
        return left;
    }
    
    public static void testListBubbleSort() {
        ListNode h1 = new ListNode();
        ListNode h2 = new ListNode();
        ListNode h3 = new ListNode();
        ListNode h4 = new ListNode();
        ListNode h5 = new ListNode();
        ListNode h6 = new ListNode();
        ListNode h7 = new ListNode();
        h1.val = 2;
        h2.val = 5;
        h3.val = 8;
        h4.val = 1;
        h5.val = 4;
        h6.val = -14;
        h7.val = 16;
        h1.next = h2;
        h2.next = h3;
        h3.next = h4;
        h4.next = h5;
        h5.next = h6;
        h6.next = h7;
        printListNode(h1);
//        printListNode(bubbleSort(h1));
//        printListNode(bubbleSortFinal1(h1));
//        printListNode(bubbleSortFinal2(h1));
          printListNode(bubbleSortSwapListNode(h1));
    }
    
    private static void printListNode(ListNode head) {
        System.out.print("[");
        for (ListNode x = head; x != null; x = x.next) {
            System.out.print(x.val + ",");
        }
        System.out.print("]");
        System.out.println();
    }
    
    private static class ListNode {
        int val;
        ListNode next;
    }
    
    public static ListNode bubbleSort(ListNode head) {
        for (ListNode x = head; x != null; x = x.next) {
            for (ListNode y = head; y != null && y.next != null; y = y.next) {
                if (y.val > y.next.val) {
                    int temp = y.val;
                    y.val = y.next.val;
                    y.next.val = temp;
                }
            }
        }
        return head;
    }
    
    public static ListNode bubbleSortFinal1(ListNode head) {
        int count = 0;
        for (ListNode x = head; x != null; x = x.next) {
            count++;
        }
        ListNode p = head;
        int N;
        while (count > 1) {
            N = count;
            // 使用变量N记录未排序元素数量，以减少比较和交换次数。
           while (p.next != null && N > 0) {
               if (p.val > p.next.val) {
                   int temp = p.val;
                   p.val = p.next.val;
                   p.next.val = temp;
               }
               p = p.next;
               N--;
           }
           p = head;
           count--;
        }
        return head;
    }
    
    public static ListNode bubbleSortFinal2(ListNode head) {
        if (head == null || head.next == null) return head;
        ListNode cur = head;
        ListNode tail = null;
        while (cur.next != tail) {
            while (cur.next != tail) {
                if (cur.val > cur.next.val) {
                    int temp = cur.val;
                    cur.val = cur.next.val;
                    cur.next.val = temp;
                }
                cur = cur.next;
            }
            // 记录最后一个已排序结点
            tail = cur;
            cur = head;
        }
        return head;
    }
    
    public static ListNode bubbleSortSwapListNode(ListNode head) {
        for (ListNode x = head; x != null; x = x.next) {
            for (ListNode y = head; y != null && y.next != null; y = y.next) {
                if (y.val > y.next.val) {
                    // swap 
                    ListNode next = y.next;
                    y.next = next.next;
                    next.next = y;
                }
            }
        }
        return head;
    }
    
    public static List<Integer> getRow(int rowIndex) {
        List<Integer> result = new ArrayList<>();
        if (rowIndex < 1) {
            return result;
        }
        if (rowIndex < 2) {
            result.add(1);
            return result;
        }
        for (int i = 1; i <= rowIndex; i++) {
            for (int j = result.size() - 2; j >= 0; j --) {
                result.set(j + 1, result.get(j) + result.get(j + 1));
            }
            result.add(1);
        }
        return result;
    }
    
    public static void printPascalTriangle(int row) {
        int[][] pa = new int[row][];
        for (int i = 0; i < row; i++) {
            pa[i] = new int[i+1];
            for (int j = 0; j <= i; j++) {
                if (i == 0 || j == 0 || i == j) {
                    pa[i][j] = 1;
                } else {
                    pa[i][j] = pa[i - 1][j - 1] + pa[i -1][j];
                }
                System.out.print(pa[i][j] + " ");
            }
            System.out.println("");
        }
    }
    
    public static int searchInsert(int[] nums, int target) {
        int low = 0;
        int hight = nums.length - 1;
        int middle = (low + hight) / 2;
        while (target > nums[middle]) {
            if (target > nums[middle]) {
                low = middle + 1;
                middle = (low + hight) / 2;
            } else {
                return middle;
            }
        }
        return middle;
    }
    
    public static int[] plusOne(int[] digits) {
        long num = 0;
        double div = Math.pow(10, digits.length - 1);
        for(int i = 0; i < digits.length; i++) {
            num += digits[i] * div;
            div = div / 10;
        }
          System.out.println("v = " + num);
        num += 1;
          System.out.println("v = " + num);
        List<Integer> rl = new ArrayList<>();
        while (num > 0) {
            int s = (int) (num % 10);
          System.out.println("v = " + s);
            rl.add(s);
            num = num / 10;
        }
        Collections.reverse(rl);
        int[] ret = new int[rl.size()];
        for (int i = 0; i < ret.length; i++) {
          System.out.println("result = " + rl.get(i));
            ret[i] = rl.get(i).intValue();
        }
        return ret;
    }
    
    public static List<String> subdomainVisits(String[] cpdomains) {
        HashMap<String, Integer> pdmap = new HashMap<>();
        for (String cpdomain : cpdomains) {
            String[] cp = cpdomain.split(" ");
            int subCount = Integer.parseInt(cp[0]);
            String subCp = cp[1];
            if (!pdmap.containsKey(subCp)) {
                pdmap.put(subCp, subCount);
            } else {
                pdmap.put(subCp, pdmap.get(subCp) + subCount);
            }
            while (subCp.indexOf(".") != -1) {
                String subS = subCp.substring(subCp.indexOf(".") + 1, subCp.length());
                if (!pdmap.containsKey(subS)) {
                    pdmap.put(subS, subCount);
                } else {
                    pdmap.put(subS, pdmap.get(subS) + subCount);
                }
                subCp = subS;
            }
        }
        List<String> rl = new ArrayList<>();
        for (String k : pdmap.keySet()) {
            rl.add(pdmap.get(k) + " " + k);
        }
        return rl;
    }
    
    public static String shortestCompletingWord(String licensePlate, String[] words) {
        int[] map = new int[26];
        char[] lc = licensePlate.toCharArray();
        int sumLetter = 0;
        for (char lci : lc) {
            if (lci >= 'A' && lci <= 'Z') {
                map[lci + 32 - 'a']++;
                sumLetter++;
            } else if (lci >= 'a' && lci <= 'z') {
                map[lci - 'a']++;
                sumLetter++;
            }
        }
        String res = "";
        for (String word : words) {
            int total = sumLetter;
            int[] wp = Arrays.copyOf(map, map.length);
            for (char c : word.toCharArray()) {
                if (--wp[c - 'a'] >= 0) --total;
            }
            if (total == 0 && (res.isEmpty() || res.length() > word.length())) {
                res = word;
            }

            
        }
        return res;
    }
    
    public static boolean isIsomorphic(String s, String t) {
        HashMap<Character, Character> map = new HashMap<>();
        char[] ss = s.toCharArray();
        char[] tt = t.toCharArray();
        for(int i = 0; i < ss.length; i++) {
            char cs = ss[i];
            char ct = tt[i];
            if (!map.containsKey(cs) && !map.containsValue(ct)) {
                map.put(cs, ct);
            } else {
                if (map.get(cs) == null || map.get(cs) != ct) {
                    return false;
                }
            }
        }
        return true;
    }
    
    public static List<String> generateParenthesis2(int n) {
        List<String> res = new ArrayList<>();
        backtrack("(", res, 1, 2);
        return res;
    }

    public static void backtrack(String sublist, List<String> res, int left, int right) {
        if (left == 0 && right == 0) {
            res.add(sublist);
            return;
        }
        if (left > right)
            return;
        if (left > 0)
            backtrack(sublist + "(", res, left - 1, right);
        if (right > 0)
            backtrack(sublist + ")", res, left, right - 1);
    }
}
