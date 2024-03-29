---
date: "2016-12-16"
type: Post
category: Android
slug: android-activity-lifecycle
tags: []
title: Android活动生命周期
status: Published
urlname: d6248408-342d-49c8-815f-69ff4076bb79
updated: "2023-07-17 15:10:00"
---

### 任务(Task)

Android 是使用任务（Task）来管理活动的，一个任务就是一组存放在栈里的活动的集合，这个栈也被称作返回栈（Back Stack）.在默认情况下，每当我们启动了一个新的活动，它会在返回栈中入栈，并处于栈顶的位置。而每当我们按下 Back 键或调用 finish()方法去销毁一个活动时，处于栈顶的活动会出栈，这时前一个入栈的活动就会重新处于栈顶的位置。系统总是会显示处于栈顶的活动给用户。

### 活动状态

Activity 类中定义了七个回调方法:

1. 运行状态: 当一个活动位于返回栈的栈顶时，这时活动就处于运行状态
2. 暂停状态: 当一个活动不再处于栈顶位置，但仍然可见时，这时活动就进入了暂停状态
3. 停止状态: 当一个活动不再处于栈顶位置，并且完全不可见的时候，就进入了停止状态，当其他地方需要内存时，处于停止状态的活动有可能会被系统回收
4. 销毁状态当一个活动从返回栈中移除后就变成了销毁状态，系统会最倾向于回收处于这种状态的活动，从而保证手机的内存充足

### 七个回调方法

Activity 类中定义了七个回调方法，覆盖了活动生命周期的每一个环节.

### onCreate()

这个方法你已经看到过很多次了，每个活动中我们都重写了这个方法，它会在活动第一次被创建的时候调用。你应该在这个方法中完成活动的初始化操作，比如说加载布局、绑定事件等。

### onStart()

这个方法在活动由不可见变为可见的时候调用。

### onResume()

这个方法在活动准备好和用户进行交互的时候调用。此时的活动一定位于返回栈的
栈顶，并且处于运行状态。

### onPause()

这个方法在系统准备去启动或者恢复另一个活动的时候调用。我们通常会在这个方
法中将一些消耗 CPU 的资源释放掉，以及保存一些关键数据，但这个方法的执行速度
一定要快，不然会影响到新的栈顶活动的使用。

### onStop()

这个方法在活动完全不可见的时候调用。它和 onPause()方法的主要区别在于，如
果启动的新活动是一个对话框式的活动，那么 onPause()方法会得到执行，而 onStop()
方法并不会执行。

### onDestroy()

这个方法在活动被销毁之前调用，之后活动的状态将变为销毁状态。

### onRestart()

这个方法在活动由停止状态变为运行状态之前调用，也就是活动被重新启动了。

### 三种生存期

以上七个方法中除了 onRestart()方法，其他都是两两相对的，从而又可以将活动分为三种生存期。

1. 完整生存期
   活动在 onCreate()方法和 onDestroy()方法之间所经历的，就是完整生存期。一般情况下，一个活动会在 onCreate()方法中完成各种初始化操作，而在 onDestroy()方法中完成释放内存的操作。
2. 可见生存期
   活动在 onStart()方法和 onStop()方法之间所经历的，就是可见生存期。在可见生存期内，活动对于用户总是可见的，即便有可能无法和用户进行交互。我们可以通过这两个方法，合理地管理那些对用户可见的资源。比如在 onStart()方法中对资源进行加载，而在 onStop()方法中对资源进行释放， 从而保证处于停止状态的活动不会占用过多内存。
3. 前台生存期
   活动在 onResume()方法和 onPause()方法之间所经历的，就是前台生存期。在前台生存期内，活动总是处于运行状态的，此时的活动是可以和用户进行相互的，我们平时看到和接触最多的也这个状态下的活动。

Android 官方提供了一张活动生命周期的示意图:

![image](../../images/e388728d5ed42b45b9fa1a9fdec1e827.png)

### 活动的启动模式

启动模式一共有四种，分别是 standard、singleTop、singleTask 和 singleInstance，可以在 AndroidManifest.xml 中通过给<activity>标签指定 android:launchMode 属性来选择启动模式。

### standard

在 standard 模式（即默认情况）下，每当启动一个新的活动，它就会在返回栈中入栈，并处于栈顶的位置。对于使用 standard 模式的活动，系统不会在乎这个活动是否已经在返回栈中存在，每次启动都会创建该活动的一个新的实例。

### singleTop

当活动的启动模式指定为 singleTop，在启动活动时如果发现返回栈的栈顶已经是该活动，则认为可以直接使用它，不会再创建新的活动实例。但并未处于栈顶时，仍会创建新的实例。

### singleTask

当活动的启动模式指定为 singleTask，每次启动该活动时系统首先会在返回栈中检查是否存在该活动的实例，如果发现已经存在则直接使用该实例，并把在这个活动之上的所有活动统统出栈，如果没有发现就会创建一个新的活动实例。

### singleInstance

指定为 singleInstance 模式的活动会启用一个新的返回栈来管理这个活动。如果我们想实现其他程序和我们的程序可以共享这个活动的实例，在这种模式下会有一个单独的返回栈来管理这个活动，不管是哪个应用程序来访问这个活动，都共用的同一个返回栈，也就解决了共享活动实例的问题。

### 利用集合类来管理活动

通过定义一个集合类来管理活动, 可方便的实现一键退出所有的活动。

```text
public class ActivityCollector {
    public static List<Activity> activities = new ArrayList<Activity>();

    public static void addActivity(Activity activity) {
        activities.add(activity);
    }

    public static void removeActivity(Activity activity) {
        activities.remove(activity);
    }

    public static void finishAll() {
        for (Activity activity : activities) {
            if (!activity.isFinishing()) {
                activity.finish();
            }
        }
    }

}

```
