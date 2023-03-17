package com.example.soilmonitoring;

import android.os.Bundle;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class Try extends AppCompatActivity {
    TextView temp,umid,soyl,moyst,nitrogen,phos,potassium;
    DatabaseReference reference;
    String status;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getSupportActionBar() != null){
            getSupportActionBar().hide();
        }
        setContentView(R.layout.activity_try);

        temp = findViewById(R.id.textView);
        umid = findViewById(R.id.hoomid);
        soyl = findViewById(R.id.soyltemp);
        moyst = findViewById(R.id.mustore);
        nitrogen = findViewById(R.id.nitroText);
        phos = findViewById(R.id.phospoText);
        potassium = findViewById(R.id.potassiumText);



        reference = FirebaseDatabase.getInstance().getReference();
        reference.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                status = snapshot.child("Temperature").getValue().toString();
                temp.setText(status);
                status = snapshot.child("Humidity").getValue().toString();
                umid.setText(status);
                status = snapshot.child("SoilTemperature").getValue().toString();
                soyl.setText(status);
                status = snapshot.child("SoilMoisture").getValue().toString();
                moyst.setText(status);
                status = snapshot.child("Nitrogen").getValue().toString();
                nitrogen.setText(status);
                status = snapshot.child("Phosphorus").getValue().toString();
                phos.setText(status);
                status = snapshot.child("Potassium").getValue().toString();
                potassium.setText(status);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });

    }
}