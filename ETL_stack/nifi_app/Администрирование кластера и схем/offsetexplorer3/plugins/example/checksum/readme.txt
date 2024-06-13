This example shows how to build a custom message decorator for Offset Explorer. This allows you to view messages that are not natively understood by Offset Explorer, in a format that you see fit.
For example, one can write a decorator for Thrift messages that will show the actual contents of the Thrift objects in a suitable format.

The provided example is a simple decorator that shows the checksum of the message bytes. The source code is located in the 'src' directory. 

Developing
----------
You need to create a class that implements the com.offsetexplorer.external.ICustomMessageDecorator2 interface. The interface is located in the 'src' directory and it has two methods that you need to implement

  public String getDisplayName();
  -This method should return a name that will be shown in the Offset Explorer's topic configuration screen where you can pick the content type for the selected topic.
  
  public String decorate(String zookeeperHost, String brokerHost, String topic, long partitionId, long offset, byte[] msg, Map<String, byte[]> headers, Map<String, String> reserved);
  -This method does the actual conversion from a byte array to a String that contains the desired output. The String may contain newlines. You should not throw any exceptions from this method, you should catch 
   all throwables in a try/catch block in your implementation. The 'reserved' argument is currently not used but may contain data in future releases.


Compiling
---------
You must compile your source code using Java 11 compatible compiler. The example 'compile.cmd' command can be used as a starting point.

Packaging
---------
You must put your own compiled classes and any dependencies you might have (e.g. Thrift libraries) into a SINGLE jar. Do not include any jars that are already in the 'lib' directory of Offset Explorer, especially any 
Apache Kafka jars. You can use the sample 'buildJar.cmd' command as a starting point.

Usage
-----
Once you have compiled and packaged your jar, copy it to the 'plugins' folder in the Offset Explorer installation folder. 
Restart Offset Explorer and navigate to the topic that you want to use the decorator with. In the 'Content Types' drop-downs you should see the name of your decorator. Select it and click on 'Update'. After that,
the messages/keys will be decorated using your custom decorator.