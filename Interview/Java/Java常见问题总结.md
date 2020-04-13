### Java常见问题总结

1. StringBuffer, StringBuilder区别

	StringBuffer是线程安全的可变字符序列，StringBuilder是线程不安全的可变字符序列（JDK1.5引入）。 用来替换需要频繁对String进行操作的场景。 
2. 什么是JVM

	JVM（java virtual machine）是一个虚拟机，它使计算机能够运行java程序，jvm就像一个运行引擎调用java代码的main方法。jvm必须实现计算机系统的规范。Java代码有JVM编译成字节码，字节码是接近月机器语言的机器无关代码。
3. JVM分配了多种类型的内存区域

	JVM分配了如下几种类型的内存区域
	Class(Method)Area: 存储着类结构,如：运行期常量、字段、方法数据和方法代码。
	Heap: 运行时数据区，对象内存分配区。
	Stack: 存储帧，包含局部变量和部分返回结果，在方法调用和返回时起作用。每个线程都拥有一个JVM栈，在线程创建时创建，方法调用时一个新帧创建，方法调用完成时帧被销毁。
	PC(program counter) register:程序计数器包含当前正在执行JVM指令的地址。
	Native method Stack: 包含所有的本地方法。
4. Classloader是什么

	Classloader是JVM的一个子系统用来加载class类文件。每当我们运行java程序时，它首先有类加载器加载。 Java有三种内置的classloader.
	Bootstrap Classloader: 第一个类加载器，它是Extension Classloader父类。拥有加载rt.jar文件。该文件包含Java Standard Edition的所有类文件，如：java.lang包类、java.net包类、java.uitil包类、java.io包类、java.sql包类等。
	Extension Classloader: 它时Bootstrap Classloader子类和System/Application Classloader父类，它加载位于$JAVA_HOME/jre/lib/ext目录中的jar文件。
	System/Application Classloader:它时Extension Classloder子类加载器。它从类路径加载类文件。默认情况下，类路径设置为当前目录。你可以使用‘-cp’或‘-classpath’开关更改类路径。
5. 静态方法和变量的目的是什么？

	静态方法和变量被所有对象之间共享。静态是类的一部分而不是类对象的一部分。静态变量存储在Class(Method) area区域中，我们不需要创建对象来访问这些变量。 在所有对象共有变量和方法时，可以使用static。

6. 默认构造函数的作用是什么？

	为对象分配默认值，如果类中没有构造函数，java编译器会隐式的创建默认构造函数。