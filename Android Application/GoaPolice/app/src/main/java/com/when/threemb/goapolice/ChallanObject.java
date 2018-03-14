package com.when.threemb.goapolice;

/**
 * Created by User on 3/13/2018.
 */

public class ChallanObject {
    private String LPNo,name,rules;
    private int amt,docNo;

    public int getDocNo() {
        return docNo;
    }

    public void setDocNo(int docNo) {
        this.docNo = docNo;
    }

    public String getLPNo() {
        return LPNo;
    }

    public void setLPNo(String LPNo) {
        this.LPNo = LPNo;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getRules() {
        return rules;
    }

    public void setRules(String rules) {
        this.rules = rules;
    }

    public int getAmt() {
        return amt;
    }

    public void setAmt(int amt) {
        this.amt = amt;
    }
}
