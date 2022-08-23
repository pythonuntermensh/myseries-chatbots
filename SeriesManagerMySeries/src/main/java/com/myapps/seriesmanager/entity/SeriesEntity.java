package com.myapps.seriesmanager.entity;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

@Entity
public class SeriesEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column
    private String name;

    @Column
    private String lowRegisterName;

    @Column
    private String additional;

    @Column
    private String VKSubscribers;

    @Column
    private String TGSubscribers;

    public SeriesEntity() {
    }

    public SeriesEntity(String name, String additional) {
        this.name = name;
        this.lowRegisterName = name.toLowerCase(Locale.ROOT);
        this.additional = additional;
        this.VKSubscribers = "";
        this.TGSubscribers = "";
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getLowRegisterName() {
        return lowRegisterName;
    }

    public void setLowRegisterName(String lowRegisterName) {
        this.lowRegisterName = lowRegisterName;
    }

    public String getAdditional() {
        return additional;
    }

    public void setAdditional(String additional) {
        this.additional = additional;
    }

    public List<Long> getVKSubscribers() {
        List<Long> result = new ArrayList<>();

        if (!VKSubscribers.isEmpty()) {
            for (String id : VKSubscribers.split(";")) {
                result.add(Long.parseLong(id));
            }
        }

        return result;
    }

    public List<Long> getTGSubscribers() {
        List<Long> result = new ArrayList<>();

        if (!TGSubscribers.isEmpty()) {
            for (String id : TGSubscribers.split(";")) {
                result.add(Long.parseLong(id));
            }
        }

        return result;
    }

    public List<Long> getSubscribers(boolean vk) {

        List<Long> result = new ArrayList<>();

        String subscribers = VKSubscribers;

        if (!vk) {
            subscribers = TGSubscribers;
        }

        if (!subscribers.isEmpty()) {
            for (String id : subscribers.split(";")) {
                result.add(Long.parseLong(id));
            }
        }

        return result;
    }

    public void setSubscribers(List<Long> subscribers, boolean vk) {

        ArrayList<String> result = new ArrayList<>();

        for (Long id : subscribers) {
            result.add(id.toString());
        }

        String subscribersResult = String.join(";", result);

        if (vk) {
            this.VKSubscribers = subscribersResult;
        } else {
            this.TGSubscribers = subscribersResult;
        }

    }

}
