package com.when.threemb.goapolice;

//import android.Manifest;
import android.content.Intent;
//import android.content.pm.PackageManager;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
//import android.provider.MediaStore;
//import android.support.v4.app.ActivityCompat;
//import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.io.ByteArrayOutputStream;
import java.util.HashMap;
import java.util.Map;

public class Challan extends AppCompatActivity implements CompoundButton.OnCheckedChangeListener,AdapterView.OnItemSelectedListener {
    private static final int RC_PHOTO_PICKER = 1888;
    Uri image;
    ImageButton numplate,doc;
    ChallanObject co;
    TextView amtView;
    Button submit;
    Spinner doclist;
    String REGISTER_URL="http://8e0f2757.ngrok.io/image";
    int buttonNo=0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_challan);
        numplate = (ImageButton) findViewById(R.id.imageButton);
        doc = (ImageButton) findViewById(R.id.docButton);
        amtView = (TextView) findViewById(R.id.amtView);
        submit = (Button) findViewById(R.id.submit);
        doclist=(Spinner)findViewById(R.id.doclist);
        co = new ChallanObject();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.logout, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == R.id.action_settings) {
            Toast.makeText(this, "Logging Out", Toast.LENGTH_LONG).show();
            SharedPreferences sp=getSharedPreferences("LoginStatus",MODE_PRIVATE);
            SharedPreferences.Editor editor=sp.edit();
            editor.putBoolean("Login",false);
            editor.apply();
            //Launch Activity
            Intent intent=new Intent(Challan.this,MainActivity.class);
            startActivity(intent);
            finish();
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    //OnClick for ImageButton
    public void uploadClick(View view) {
        if(view.getId()==R.id.imageButton)
        {buttonNo=1;}
        else if(view.getId()==R.id.docButton)
        {buttonNo=2;}
        else
        {buttonNo=0;}

        Intent intent1 = new Intent(Intent.ACTION_GET_CONTENT);
        intent1.setType("image/jpeg");
        intent1.putExtra(Intent.EXTRA_LOCAL_ONLY, true);
        startActivityForResult(Intent.createChooser(intent1, "Complete action using"), RC_PHOTO_PICKER);

        //USING CAMERA APP
        /*Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[] { Manifest.permission.CAMERA}, 0);
        }
        else
            startActivityForResult(Intent.createChooser(intent, "Complete action using"), RC_PHOTO_PICKER);*/
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == RC_PHOTO_PICKER && resultCode == RESULT_OK) {
            image = data.getData();
            //Number Plate Button Clicked
            //Bitmap photo = (Bitmap) data.getExtras().get("data"); //FOR CAMERA APP
            if(buttonNo==1){
            numplate.setImageURI(image);
            sendImageToServer();
            loadLayout("WB29AF1234");
            }
            else //Document Button Clicked
            {
                doc.setImageURI(image);
                buttonNo=3;
            }

        }
    }

    //Sending Driver Plate For Recognition
    public void sendImageToServer() {
        Bitmap bitmap = ((BitmapDrawable) numplate.getDrawable()).getBitmap();
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, baos);
        byte[] imageBytes = baos.toByteArray();
        final String imageString = Base64.encodeToString(imageBytes, Base64.DEFAULT);

        StringRequest stringRequest = new StringRequest(Request.Method.POST, REGISTER_URL,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        //Toast.makeText(LoginActivity.this, response+"Sent successfully !", Toast.LENGTH_LONG).show();
                        //request initial/name/dept
                        Toast.makeText(Challan.this, "Recieved: " + response, Toast.LENGTH_SHORT).show();

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(Challan.this, "FAILED " + error.toString(), Toast.LENGTH_LONG).show();
                    }
                }) {
            @Override
            protected Map<String, String> getParams() {
                Map<String, String> params = new HashMap<String, String>();
                params.put("image", imageString);
                return params;
            }

        };

        RequestQueue requestQueue = Volley.newRequestQueue(this);
        stringRequest.setRetryPolicy(new DefaultRetryPolicy(10000,2, (float) 1.5));
        requestQueue.add(stringRequest);


    }



    //Load remaining Components for the Layout
    public void loadLayout(String lpno) {
        co.setLPNo(lpno);
        String rules = "";
        final EditText et = (EditText) findViewById(R.id.lpno);
        et.setText(co.getLPNo());
        doclist.setOnItemSelectedListener(this);

        //Creating Violation Checkbox list
        final LinearLayout ll = (LinearLayout) findViewById(R.id.llcb);
        String[] arr = getResources().getStringArray(R.array.rules);
        for (int i = 0; i < arr.length; i++) {
            rules += "0";
            CheckBox ch = new CheckBox(this);
            ch.setId(i);
            ch.setText(arr[i]);
            ch.setOnCheckedChangeListener(this);
            ll.addView(ch);
        }
        co.setRules(rules);
    }

    //Violation Checkbox Click Listener
    @Override
    public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
        String change = b ? "1" : "0";
        String temp = co.getRules();
        int ind = compoundButton.getId();
        temp = temp.substring(0, ind) + change + temp.substring(ind + 1);
        co.setRules(temp);
        Toast.makeText(this, temp, Toast.LENGTH_SHORT).show();

        co.setAmt(co.getAmt() + (b ? 100 : -100));
        amtView.setText("Amount: " + co.getAmt());

        if (co.getAmt() == 0)
        {
            submit.setVisibility(View.INVISIBLE);
            doclist.setVisibility(View.INVISIBLE);
            doc.setVisibility(View.INVISIBLE);
        }
        else
        {
            submit.setVisibility(View.VISIBLE);
            doclist.setVisibility(View.VISIBLE);
            doc.setVisibility(View.VISIBLE);
            buttonNo=0;
            doc.setImageResource(R.mipmap.ic_launcher);

        }
    }

    //Submit Button Click Listener
    public void Submit(View view) {
        if(co.getDocNo()==0 || buttonNo!=3)
            Toast.makeText(this, "No Document Found"+buttonNo+co.getDocNo(), Toast.LENGTH_SHORT).show();
        else
            Toast.makeText(this, "Submitted", Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
        co.setDocNo(i);
        Toast.makeText(this, "Doc:"+i, Toast.LENGTH_SHORT).show();
        doc.setVisibility(View.VISIBLE);
    }

    @Override
    public void onNothingSelected(AdapterView<?> adapterView) {
        co.setDocNo(0);
    }
}
