package com.myapps.seriesmanager.entity;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Entity
public class SubscribersNewSeriesEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column
    private String TGSubs;

    @Column
    private String VKSubs;

    public SubscribersNewSeriesEntity() {
        this.TGSubs = "";
        this.VKSubs = "";
    }

    public Long getId() {
        return id;
    }

    public List<Long> getTGSubs() {
        List<Long> result = new ArrayList<>();

        if (!TGSubs.isEmpty()) {
            for (String id : TGSubs.split(";")) {
                result.add(Long.parseLong(id));
            }
        }

        return result;
    }

    public List<Long> getVKSubs() {
        List<Long> result = new ArrayList<>();

        if (!VKSubs.isEmpty()) {
            for (String id : VKSubs.split(";")) {
                result.add(Long.parseLong(id));
            }
        }

        return result;
    }

    public void setTGSubs(List<Long> TGSubs) {
        List<String> result = TGSubs.stream().map(Object::toString).toList();
        this.TGSubs = String.join( ";", result);
    }

    public void setVKSubs(List<Long> VKSubs) {
        List<String> result = VKSubs.stream().map(Object::toString).toList();
        this.VKSubs = String.join( ";", result);
    }
}
