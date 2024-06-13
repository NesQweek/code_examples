package com.offsetexplorer.external;

import java.util.Map;
import java.util.zip.CRC32;

public class ChecksumDecorator implements ICustomMessageDecorator2 {
  private CRC32 crc32;

  public ChecksumDecorator() {
    this.crc32 = new CRC32();
  }

  @Override
  public String getDisplayName() { return "Checksum"; }

  @Override
  public String decorate(String zookeeperHost, String brokerHost, String topic, long partitionId, long offset, byte[] msg, Map<String, byte[]> headers, Map<String, String> reserved) {
    try {
      crc32.reset();
      crc32.update(msg);

      return "Checksum= \n" + crc32.getValue();
    } catch(Throwable t) {
      return "Error: " + t.getMessage();
    }
  }
}
