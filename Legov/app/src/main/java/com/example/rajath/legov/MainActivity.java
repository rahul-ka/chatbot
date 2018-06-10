package com.example.rajath.legov;

import android.os.AsyncTask;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ListView;

import com.example.rajath.legov.Adapter.CustomAdapter;
import com.example.rajath.legov.Model.ChatModel;
import com.example.rajath.legov.Model.LegovModel;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

import co.devcenter.androiduilibrary.ChatView;

public class MainActivity extends AppCompatActivity {

    ListView listView;
    EditText editText;
    List<ChatModel> list_chat = new ArrayList<>();
    FloatingActionButton btn_send_message;
    private static final String URL = "https://legal-service-bot.herokuapp.com/REST_API/message/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.chat_view);

        listView = (ListView) findViewById(R.id.list_of_message);
        editText = (EditText)findViewById(R.id.user_message);
        btn_send_message = (FloatingActionButton) findViewById(R.id.fab);

        btn_send_message.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String text = editText.getText().toString();
                ChatModel chatModel = new ChatModel(text,true);
                list_chat.add(chatModel);
                new ChatBot().execute(list_chat);

                editText.setText("");
            }
        });
    }

    private class ChatBot extends AsyncTask<List<ChatModel>,Void,String> {
        String stream = null;
        List<ChatModel> models;
        String text = editText.getText().toString();
        String reply;

        @Override
        protected String doInBackground(List<ChatModel>... lists) {
            models = lists[0];
            JSONObject jsonObjSend = new JSONObject();
            reply = "error";

            try {
                jsonObjSend.put("message", text);

                Log.e("\n\nRequest JSON build", text + "\n\n");

            } catch (JSONException e) {
                e.printStackTrace();
            }
            reply = HttpClient.SendHttpPost(URL, jsonObjSend);
            Log.e("\n\nAfter POST CALL","\n\n" + reply + "\n\n");

            return reply;
        }

        @Override
        protected void onPostExecute(String s) {
            LegovModel response = new LegovModel(s);
            ChatModel chatModel = new ChatModel(response.getReply(),false);
            models.add(chatModel);
            CustomAdapter customAdapter = new CustomAdapter(models,getApplicationContext());
            listView.setAdapter(customAdapter);
        }
    }
}
