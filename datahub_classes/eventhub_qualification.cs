using fa_eventhub_to_sonia.models.common;
using Newtonsoft.Json;
using System;

namespace fa_eventhub_to_sonia.models.events {
    public class Qualification {
        [JsonProperty("qualificationId")]
        public string QualificationId { get; set; }

        [JsonProperty("code")]
        public string Code { get; set; }

        [JsonProperty("title")]
        public string Title { get; set; }

        [JsonProperty("shortTitle")]
        public string ShortTitle { get; set; }

        [JsonProperty("level")]
        public string Level { get; set; }

        [JsonProperty("faculty")]
        public QualificationFaculty Faculty { get; set; }

        [JsonProperty("duration")]
        public float Duration { get; set; }

        [JsonProperty("eftsValue")]
        public int EFTSValue { get; set; }

        [JsonProperty("subjects")]
        public QualificationSubject[] Subjects { get; set; }

        [JsonProperty("nzqfLevel")]
        public string NZQFLevel { get; set; }
        
        [JsonProperty("nzsced")]
        public GenericCodeDesc NZSced { get; set; }

        [JsonProperty("award")]
        public Award Award { get; set; }

        [JsonProperty("programmeGroup")]
        public string ProgrammeGroup { get; set; }

        [JsonProperty("type")]
        public string Type { get; set; }

        [JsonProperty("createdDate")]
        [JsonConverter(typeof(DateFormatter), "yyyy-MM-dd")]
        public DateTime CreatedDate { get; set; }

        [JsonProperty("retirementDate")]
        [JsonConverter(typeof(DateFormatter), "yyyy-MM-dd")]
        public DateTime RetirementDate { get; set; }

        [JsonProperty("status")]
        public string Status { get; set; }

        [JsonProperty("isPostGraduate")]
        public bool IsPostGraduate { get; set; }
    }

    public class QualificationFaculty {
        [JsonProperty("code")]
        public string Code { get; set; }

        [JsonProperty("faculty")]
        public string Faculty { get; set; }
    }

    public class QualificationSubject {
        [JsonProperty("subject")]
        public string Subject { get; set; }

        [JsonProperty("type")]
        public string Type { get; set; }

        [JsonProperty("code")]
        public string Code { get; set; }

        [JsonProperty("qualification")]
        public string Qualification { get; set; }
    }

    public class Award {
        [JsonProperty("categoryCode")]
        public string CategoryCode { get; set; }

        [JsonProperty("categoryDescription")]
        public string CategoryDescription { get; set; }
    }

}