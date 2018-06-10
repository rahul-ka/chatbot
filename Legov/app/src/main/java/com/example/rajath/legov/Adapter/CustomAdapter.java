package com.example.rajath.legov.Adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;

import com.example.rajath.legov.Model.ChatModel;
import com.example.rajath.legov.R;
import com.github.library.bubbleview.BubbleTextView;

import java.util.List;

public class CustomAdapter extends BaseAdapter {

    private List<ChatModel> list_chat_models;
    private Context context;
    private LayoutInflater layoutInflater;

    public CustomAdapter(List<ChatModel> list_chat_models, Context context) {
        this.list_chat_models = list_chat_models;
        this.context = context;
        layoutInflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    }

    @Override
    public int getCount() {
        return list_chat_models.size();
    }

    @Override
    public Object getItem(int i) {
        return list_chat_models.get(i);
    }

    @Override
    public long getItemId(int i) {
        return i;
    }

    @Override
    public View getView(int i, View view, ViewGroup viewGroup) {
        View contextView = view;
        if (contextView == null){
            if (list_chat_models.get(i).isSend)
                view = layoutInflater.inflate(R.layout.list_item_message_send,null);
            else
                view = layoutInflater.inflate(R.layout.list_item_message_recv,null);

            BubbleTextView text_message = (BubbleTextView) view.findViewById(R.id.text_message);
            text_message.setText(list_chat_models.get(i).message);
        }
        return view;
    }
}
