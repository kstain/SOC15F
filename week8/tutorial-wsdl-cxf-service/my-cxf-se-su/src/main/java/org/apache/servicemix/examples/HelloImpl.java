/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.servicemix.examples;
 
import javax.jws.WebService;
import javax.xml.ws.Holder;
 
import org.apache.servicemix.examples.types.SayHello;
import org.apache.servicemix.examples.types.SayHelloResponse;
 
@WebService(serviceName = "HelloService", targetNamespace = "http://servicemix.apache.org/examples", endpointInterface = "org.apache.servicemix.examples.Hello")
public class HelloImpl implements Hello {
 
    public void sayHello(Holder<String> name)
        throws UnknownWordFault
    {
        if (name.value == null || name.value.length() == 0) {
           org.apache.servicemix.examples.types.UnknownWordFault fault = new org.apache.servicemix.examples.types.UnknownWordFault();
            throw new UnknownWordFault(null, fault);
        }
  
      name.value = "Hi " + name.value;
    }
 
}
