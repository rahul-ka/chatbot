package com.example.rajath.legov;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONObject;
import android.util.Log;

public class HttpClient {

    private static final String TAG = "HttpClient";

    public static String SendHttpPost(String URL, JSONObject jsonObjSend) {
        JSONObject reply = new JSONObject();
        try {
            Log.e("\n\nJSON built", jsonObjSend.toString());
            reply.put("reply","Error");
            DefaultHttpClient httpclient = new DefaultHttpClient();
            HttpPost httpPostRequest = new HttpPost(URL);
            StringEntity se;
            se = new StringEntity(jsonObjSend.toString());

            // Set HTTP parameters
            httpPostRequest.setEntity(se);

            long t = System.currentTimeMillis();
            HttpResponse response = (HttpResponse) httpclient.execute(httpPostRequest);
            Log.i("\n\n" + TAG, "HTTPResponse received in [" + (System.currentTimeMillis()-t) + "ms]\n\n");

            Log.i("\n\n" + "Response", "\n\n" + response.toString() + "\n\n");
            // Get hold of the response entity (-> the data):
            HttpEntity entity = response.getEntity();

            Log.i("\n\n" + "Response Entity", "\n\n" + entity.toString() + "\n\n");

            if (entity != null) {
                // Read the content stream
                InputStream instream = entity.getContent();

                Log.i("\n\n" + "instream", "\n\n" + instream.toString() + "\n\n");

                // convert content stream to a String
                String resultString= convertStreamToString(instream);
                Log.i("\n\nResponse", resultString);
                instream.close();
                resultString = resultString.substring(1,resultString.length()-2); // remove wrapping "[" and "]"
                Log.i("\n\nAnother Response", resultString);
                String newResultString[] = resultString.split(":");
                resultString = newResultString[1].substring(2,newResultString[1].length()-1);
                Log.i("\n\nAfter Split", resultString);
                // Transform the String into a JSONObject

                return resultString;
            }

        }
        catch (Exception e)
        {
            // More about HTTP exception handling in another tutorial.
            // For now we just print the stack trace.
            e.printStackTrace();
        }
        return "Error";
    }


    private static String convertStreamToString(InputStream is) {

        BufferedReader reader = new BufferedReader(new InputStreamReader(is));
        StringBuilder sb = new StringBuilder();

        String line = null;
        try {
            while ((line = reader.readLine()) != null) {
                sb.append(line + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                is.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return sb.toString();
    }

}
