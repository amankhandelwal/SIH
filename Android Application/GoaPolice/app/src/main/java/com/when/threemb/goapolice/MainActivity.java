package com.when.threemb.goapolice;

import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    EditText editTextUsername,editTextPassword;
    String REGISTER_URL="http://8e0f2757.ngrok.io/login";
    SharedPreferences sp;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        editTextUsername=(EditText)findViewById(R.id.username);
        editTextPassword=(EditText)findViewById(R.id.password);
        sp=getSharedPreferences("LoginStatus",MODE_PRIVATE);

        if(sp.getBoolean("Login",false))
        {
            Intent intent=new Intent(MainActivity.this,Challan.class);
            startActivity(intent);
        }


    }
    public void loginClick(View view) {
        final String username = editTextUsername.getText().toString().trim();
        final String password = editTextPassword.getText().toString().trim();

        if (username.length()!=0 && password.length()!=0) {

            StringRequest stringRequest = new StringRequest(Request.Method.POST, REGISTER_URL,
                    new Response.Listener<String>() {
                        @Override
                        public void onResponse(String response) {
                            //Toast.makeText(LoginActivity.this, response+"Sent successfully !", Toast.LENGTH_LONG).show();
                            //request initial/name/dept
                            Toast.makeText(MainActivity.this, "Recieved "+response, Toast.LENGTH_SHORT).show();

                            if(response.equalsIgnoreCase("Failed"))
                            {
                                Toast.makeText(MainActivity.this,"Incorrect Credentials", Toast.LENGTH_LONG).show();
                            }
                            else if(response.equalsIgnoreCase("Success")) {
                                Toast.makeText(MainActivity.this, "Logged In", Toast.LENGTH_SHORT).show();
                                //Save Login State

                                SharedPreferences.Editor editor=sp.edit();
                                editor.putBoolean("Login",true);
                                editor.apply();
                                //Launch Activity
                                Intent intent=new Intent(MainActivity.this,Challan.class);
                                startActivity(intent);
                            }

                        }
                    },
                    new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            Toast.makeText(MainActivity.this, "FAILED " + error.toString(), Toast.LENGTH_LONG).show();
                        }
                    }) {
                @Override
                protected Map<String, String> getParams() {
                    Map<String, String> params = new HashMap<String, String>();
                    params.put("policeId", username);
                    params.put("password", password);
                    return params;
                }

            };

            RequestQueue requestQueue = Volley.newRequestQueue(this);
            requestQueue.add(stringRequest);
        }
        else
        {
            Toast.makeText(this,"Invalid Username/Password",Toast.LENGTH_SHORT).show();
            finish();
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        finish();
    }
}
