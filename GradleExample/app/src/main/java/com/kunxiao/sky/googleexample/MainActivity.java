package com.kunxiao.sky.googleexample;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity implements AdapterView.OnItemClickListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        GridView gridView = findViewById(R.id.grid_view);
        gridView.setAdapter(new ActivityAdapter(this));
        gridView.setOnItemClickListener(this);
    }

    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        ActivityInfo activityInfo = (ActivityInfo) parent.getItemAtPosition(position);
        if (activityInfo != null) {
            activityInfo.startActivity(this);
        }
    }

    public static class ActivityAdapter extends BaseAdapter {
        private Context context;
        private LayoutInflater layoutInflater;
        private List<ActivityInfo> activityInfoList;

        public ActivityAdapter(Context context) {
            this.context = context;
            this.layoutInflater = LayoutInflater.from(context);
            this.activityInfoList = initActivities();
        }

        @Override
        public int getCount() {
            return activityInfoList != null ? activityInfoList.size() : 0;
        }

        @Override
        public Object getItem(int position) {
            return activityInfoList.get(position);
        }

        @Override
        public long getItemId(int position) {
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            ViewHolder viewHolder;
            if (convertView == null) {
                viewHolder = new ViewHolder();
                convertView = layoutInflater.inflate(R.layout.grid_item, null);
                viewHolder.icon = convertView.findViewById(R.id.icon);
                viewHolder.text = convertView.findViewById(R.id.text);
                convertView.setTag(viewHolder);
            } else {
                viewHolder = (ViewHolder) convertView.getTag();
            }
            ActivityInfo activityInfo = (ActivityInfo) getItem(position);
            if (activityInfo != null) {
                viewHolder.icon.setImageResource(activityInfo.icon);
                viewHolder.text.setText(activityInfo.text);
            }
            return convertView;
        }

        private List<ActivityInfo> initActivities() {
            List<ActivityInfo> activityInfoList = new ArrayList<>();
            activityInfoList.add(new ActivityInfo("com.example.android.notepad.NotesList", R.mipmap.ic_launcher, R.string.app_name));
            return activityInfoList;
        }
    }

    public static class ViewHolder {
        public ImageView icon;
        public TextView text;
    }

    public static class ActivityInfo {
        public String cla;
        public int icon;
        public int text;

        public ActivityInfo(String cla, int icon, int text) {
            this.cla = cla;
            this.icon = icon;
            this.text = text;
        }

        public void startActivity(Context context) {
            Intent intent = new Intent();
            intent.setComponent(new ComponentName(context, cla));
            context.startActivity(intent);
        }
    }
}
